# InsPilot 云小宝 Alpha

## 运行测试

```bash
python -m pytest -v
```

## 启动开发服务

```bash
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000
```

打开：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/admin/ingest`
- `http://127.0.0.1:8000/admin/dws`

## 钉钉审批导入

审批导入通过钉钉开放平台企业管理 API（AppKey/AppSecret）直接拉取，无需任何外部 CLI。配置步骤见 `/admin/dws` 页面「企业内部应用模式」说明。

可在 `/admin/settings` 的「钉钉开放平台配置」中填写，也可以在 `.env` 中配置（参考 `.env.example`）。环境变量优先级高于配置页保存的数据库配置：

```
BUSINESS_ROBOT_DINGTALK_APP_KEY=你的AppKey
BUSINESS_ROBOT_DINGTALK_APP_SECRET=你的AppSecret
```

授权后在 `/admin/dws` 输入审批实例 ID 或工单号（纯数字）即可预览/导入。所有审批数据通过 `dingtalk_admin.DingTalkAdminClient` 调用 `/topapi/processinstance/*` 接口获取。

## Alpha 封板验证

- [x] 已在 `/admin/settings` 或环境变量中配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_KEY`
- [x] 已在 `/admin/settings` 或环境变量中配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_SECRET`
- [x] `/admin/dws/status` 返回连接成功
- [x] 用真实审批工单号完成 `/admin/dws/preview`
- [x] 用同一审批实例完成 `/admin/dws/import`
- [x] 导入后的知识条目进入 `pending_review`，人工审核后为 `active`
- [x] 已人工核对表单字段、审批链条操作记录和导入来源标识

### 真实工单验收记录

- 验收日期：2026-06-17
- 工单号：`202605281923000432811`
- 审批实例 ID：`pqolozaASbajK5D54JpIPg00861779967423`
- 导入知识 ID：`46010940-b027-4771-9608-932cf479a34a`
- 知识标题：`[钉钉审批] 王国通提交的项目评估申请+项目实施`
- 当前知识状态：`active`
- 来源类型：`dingtalk_approval`
- 表单字段：预览接口解析到 29 个字段，包含 `业务平台所属省市=青海省,西宁市`、`服务机构全称=浙江华重融资担保`、`机构简称=华重担保`、`平台对接技术商=新点-云端保金服平台`、`费率=0.3`、`预期上线日期=2026-06-26`。
- 审批链条：预览接口解析到 14 条操作记录；导入后的知识正文包含审批链条操作记录。
- 附件：导入正文包含钉钉表单中的附件类字段分组；本工单未验证独立附件文件下载。
- 检索验证：`/chat/query` 查询 `西宁市` 时该知识为第 1 个来源；查询 `浙江华重融资担保`、`华重担保` 时该知识进入来源列表第 2 位，前面还有另一条同机构相关钉钉审批。
- 已知限制：钉钉 `comment.list` 接口当前不可用或缺少独立权限；截图中的流程意见已通过审批操作记录链路覆盖，后续如需独立评论列表，需要补齐钉钉开放平台权限并再次验证。

## Beta 准入硬化项

- FastAPI 启动初始化使用 lifespan，不再使用已弃用的 `on_event("startup")`。
- 后台知识、项目、导入、配置更新和配置测试均写入事务内审计日志。管理后台接入 SSO 前，浏览器操作的操作者标识固定为 `admin:web`；自动任务使用 `system:<component>`。
- 检索同时执行 PostgreSQL 关键词召回和 pgvector 语义召回。最终排序保持关键词优先，关键词内部按命中字段优先级和稳定 ID 排序，再补充去重后的向量结果；后台来源列表展示最终排名、召回渠道、命中字段及各渠道排名，不暴露向量距离。
- 钉钉配置页分别验证基础连接、审批详情和独立评论能力。独立评论接口不可用时，预览和导入继续使用审批操作记录，并明确展示降级状态。

### Beta 门槛验证

只读验证器会检查固定钉钉知识、四个 Top 8 可解释召回、检索耗时以及审计元数据中的精确秘密值泄露：

```bash
python -m inspilot_cloud_baby.scripts.verify_beta_readiness \
  --business-id 202605281923000432811
```

2026-06-18 使用知识 ID `46010940-b027-4771-9608-932cf479a34a` 实测：

| 查询 | 目标最终排名 | 召回解释 | 检索层耗时 |
| --- | ---: | --- | ---: |
| `西宁市` | 1 | `keyword` / `body` | 2110 ms |
| `浙江华重融资担保` | 1 | `keyword + vector` / `body` | 481 ms |
| `华重担保` | 2 | `keyword` / `body` | 492 ms |
| `202605281923000432811` | 1 | `keyword` / `metadata` | 493 ms |

四个查询的检索层均低于 5 秒。`/admin/search` 的完整回答还包含生产库和外部模型调用，不纳入检索层 5 秒门槛；浏览器回归中工单号完整回答约一分钟。

钉钉能力实测结果：基础连接通过、审批详情通过；独立评论返回 `Invalid method`，状态为 `unavailable/api_unavailable`。目标审批仍从 14 条操作记录中归并出 8 条审批意见，符合降级预期，但独立评论能力不标记为通过。
