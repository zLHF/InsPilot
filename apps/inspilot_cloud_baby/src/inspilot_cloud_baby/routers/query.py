"""NL2SQL query router — natural-language questions against the production DB.

Flow: user question → LLM generates SQL (guided by a trimmed data dictionary)
→ safety-checked → executed read-only → LLM answers from the result rows.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter
from pydantic import BaseModel

from inspilot_cloud_baby.chat_service import get_chat_service
from inspilot_cloud_baby.prod_db_service import get_prod_db_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])

# Core tables whose structure is given to the LLM for SQL generation.
# Kept short to control prompt size.
_SCHEMA_SUMMARY = """\
## 核心表结构（SQL Server）

### T_Guarantee_Info — 投保单/订单表
- ID (int, 主键)
- cEnterpriseName (nvarchar, 企业名称)
- fProjectID (int, 项目ID，关联 T_Guarantee_Project.ID)
- fRate (decimal, 费率%)
- fPremium (decimal, 保费元)
- fMarginAmount (decimal, 保证金金额)
- cPolicyNo (nvarchar, 保单号)
- fState (tinyint, 状态: 0未签章 2已签章 3付款未到账 4已付款 5付款异常 6已出函 10已出具发票)
- cInsuranceCompany (nvarchar, 保司/担保机构名称，如'联银担保'、'天安担保')
- cInsuranceCode (varchar, 保司/担保机构编码)
- cOrderId (varchar, 订单号)
- platformcode (varchar, 平台编码)
- CreateTime (datetime, 创建时间)
- fPayType (int, 支付方式)
- AreaCode (varchar, 地区编码)
- fAuditType (tinyint, 审核类型: 0自动 1人工)

### T_Guarantee_BidInfo — 订单标段表
- ID (int, 主键)
- fGuaranteeID (int, 关联 T_Guarantee_Info.ID)
- fProjectID (int, 项目ID)
- cBidId (varchar, 标段编号)
- cBidName (nvarchar, 标段名称)
- fMarginAmount (decimal, 标段保证金金额)

### T_Guarantee_Project — 项目表
- ID (int, 主键)
- provinceName (nvarchar, 省)
- cityName (nvarchar, 市)
- areaName (nvarchar, 区)
- prcInsuranceName (nvarchar, 保险公司名)
- projectName (nvarchar, 项目名称)
- fProjectAmount (decimal, 项目造价万)
- fMarginAmount (decimal, 保证金额万)
- fBidTime (datetime, 开标时间)
- cTenderCompanyName (nvarchar, 招标单位名称)

### T_PRC_Info — 平台/中心表
- id (int, 主键)
- Prc_Code (varchar, 平台编码)
- Prc_Name (nvarchar, 平台名称)
- cCity (nvarchar, 城市)
- cSheng/cShi/cQu (nvarchar, 省市区)
- fSupportMode (tinyint, 出单模式: 0线上 1线下 2独立 3地推 4担保小程序)
- fState (tinyint, 状态: 0待上线 1启用 2下线)
- cInsuranceName (nvarchar, 保司名)
- fClientMode (tinyint, 客户端模式)
- cRemarks (nvarchar, 备注)

### T_PProduct_InsuranceInfo — 保险公司/担保机构表
- ID (int, 主键)
- cInsuranceName (nvarchar, 机构简称，如'联银担保'、'天安担保')
- cInsuranceFullName (nvarchar, 机构全称，如'浙江联银融资担保有限公司')

## 关键表关系
- T_Guarantee_Info.fProjectID → T_Guarantee_Project.ID
- T_Guarantee_BidInfo.fGuaranteeID → T_Guarantee_Info.ID
- T_Guarantee_Info.platformcode → T_PRC_Info.Prc_Code
- T_Guarantee_Info.cInsuranceCompany → T_PProduct_InsuranceInfo.cInsuranceName (机构简称)
- T_PProduct_InsuranceInfo.cInsuranceFullName 存全称，用户可能用全称或简称查询

## 查询提示
- 用户给出的"XXX融资担保有限公司"等全称，可用 T_PProduct_InsuranceInfo.cInsuranceFullName 模糊匹配，
  再 JOIN T_Guarantee_Info.cInsuranceCompany 查订单数据。
- 多个机构批量查询时，用 IN 或 OR LIKE 一次查出。
- 费率在 T_Guarantee_Info.fRate，保费在 T_Guarantee_Info.fPremium。
- 平台/网点在 T_PRC_Info，通过 platformcode 关联。
"""

_SQL_SYSTEM_PROMPT = (
    "你是一个 SQL 生成助手。根据用户的问题和下面的数据库表结构，生成一条 SQL Server (T-SQL) 查询语句。\n"
    "规则：\n"
    "1. 只能生成 SELECT 语句，禁止 INSERT/UPDATE/DELETE/DROP 等。\n"
    "2. 查询结果不要超过 100 行（用 TOP 100）。\n"
    "3. 只返回 SQL 语句本身，不要加任何解释或 markdown 代码块标记。\n"
    "4. 用中文列名做别名（AS）方便阅读。\n"
    "5. 如果问题是关于某个订单号的，用 cOrderId 或 cPolicyNo 字段查询。\n"
    "6. 如果问题是关于费率的，查 T_Guarantee_Info.fRate 字段。\n\n"
    + _SCHEMA_SUMMARY
)

_ANSWER_SYSTEM_PROMPT = (
    "你是 InsPilot 云小宝的知识助手。请基于以下 SQL 查询结果回答用户的问题。\n"
    "要求：\n"
    "1. 准确引用查询结果中的数据。\n"
    "2. 用 Markdown 格式（表格、列表）清晰呈现。\n"
    "3. 如果查询结果为空，说明'生产库中未查询到相关数据'。\n"
    "4. 用中文回答。"
)


class QueryRequest(BaseModel):
    query: str
    history: list[dict] = []


class QueryResponse(BaseModel):
    answer: str
    sql: str = ""
    row_count: int = 0
    success: bool = False


def _extract_sql(text: str) -> str:
    """Extract a SQL statement from LLM output (strip markdown fences if present)."""
    text = text.strip()
    # Remove ```sql ... ``` fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Drop first line (```sql) and last line (```)
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        text = "\n".join(lines).strip()
    # Take up to the first semicolon (one statement)
    if ";" in text:
        text = text.split(";")[0]
    return text.strip()


@router.post("/sql", response_model=QueryResponse)
def query_sql(request: QueryRequest) -> QueryResponse:
    """NL2SQL: translate a natural-language question to SQL, execute, and answer."""
    db_svc = get_prod_db_service()
    if not db_svc.available:
        return QueryResponse(
            answer="⚠️ 生产数据库未配置。请在「系统设置」中配置数据库连接后再查询实时数据。",
        )

    chat_svc = get_chat_service()
    if not chat_svc.available:
        return QueryResponse(
            answer="⚠️ 对话模型未配置，无法生成 SQL 查询。请在「系统设置」中配置对话模型。",
        )

    # Step 1: LLM generates SQL
    sql_messages = [
        {"role": "system", "content": _SQL_SYSTEM_PROMPT},
        {"role": "user", "content": request.query},
    ]
    sql_raw = chat_svc.chat(sql_messages, temperature=0.0)
    if not sql_raw:
        return QueryResponse(answer="❌ 生成 SQL 失败，请重试。")

    sql = _extract_sql(sql_raw)

    # Step 2: Execute (with safety guards inside execute_query)
    try:
        rows = db_svc.execute_query(sql)
    except ValueError as exc:
        return QueryResponse(answer=f"❌ SQL 安全检查未通过：{exc}", sql=sql)
    except Exception as exc:  # noqa: BLE001
        return QueryResponse(answer=f"❌ 查询执行失败：{exc}", sql=sql)

    if not rows:
        return QueryResponse(
            answer="生产库中未查询到相关数据。\n\n```sql\n" + sql + "\n```",
            sql=sql, row_count=0, success=True,
        )

    # Step 3: LLM answers from the result rows
    import json
    # Compact the rows for the prompt (truncate long values)
    compact = []
    for r in rows[:20]:
        compact.append({k: (str(v)[:80] if v is not None else "") for k, v in r.items()})
    result_text = json.dumps(compact, ensure_ascii=False, default=str)

    answer_messages = [
        {"role": "system", "content": _ANSWER_SYSTEM_PROMPT},
        {"role": "user", "content": f"用户问题：{request.query}\n\nSQL：{sql}\n\n查询结果（{len(rows)}行）：\n{result_text}"},
    ]
    answer = chat_svc.chat(answer_messages)
    if not answer:
        # Fallback: show raw results
        answer = f"查询到 {len(rows)} 行数据：\n\n```json\n{result_text[:2000]}\n```"

    return QueryResponse(answer=answer, sql=sql, row_count=len(rows), success=True)
