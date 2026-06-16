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

在 `.env` 中配置（参考 `.env.example`）：

```
BUSINESS_ROBOT_DINGTALK_APP_KEY=你的AppKey
BUSINESS_ROBOT_DINGTALK_APP_SECRET=你的AppSecret
```

授权后在 `/admin/dws` 输入审批实例 ID 或工单号（纯数字）即可预览/导入。所有审批数据通过 `dingtalk_admin.DingTalkAdminClient` 调用 `/topapi/processinstance/*` 接口获取。
