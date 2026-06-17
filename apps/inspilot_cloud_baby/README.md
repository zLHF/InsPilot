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
- 审计日志表 `audit_logs` 作为权限、安全和敏感操作留痕的基础。
- 真实钉钉审批导入主链路已通过一个工单验证；Beta 前仍需补齐审计写入、检索排序可解释性和独立评论接口权限验证。
