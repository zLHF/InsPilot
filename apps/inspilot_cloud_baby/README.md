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

- [ ] 已在 `/admin/settings` 或环境变量中配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_KEY`
- [ ] 已在 `/admin/settings` 或环境变量中配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_SECRET`
- [ ] `/admin/dws/status` 返回连接成功
- [ ] 用真实审批实例 ID 完成 `/admin/dws/preview`
- [ ] 用同一实例完成 `/admin/dws/import`
- [ ] 导入后的知识条目处于 `pending_review`
- [ ] 已人工核对表单字段、评论、附件元数据和来源文件名

## Beta 准入硬化项

- FastAPI 启动初始化使用 lifespan，不再使用已弃用的 `on_event("startup")`。
- 审计日志表 `audit_logs` 作为权限、安全和敏感操作留痕的基础。
- 真实钉钉审批导入验收完成前，Alpha 不应标记为封板完成。
