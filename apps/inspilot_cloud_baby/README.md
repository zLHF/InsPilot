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

## DWS PoC

企业管理员授权后运行：

```bash
dws auth login
dws schema oa --format json
dws oa process-instance get --instance-id "PROC-EXAMPLE-001" --format json
```

实际 OA 命令必须以 `dws schema oa --format json` 返回结果为准。如果命令名或参数不同，更新 `inspilot_cloud_baby.dws_adapter.DwsAdapter` 和对应测试。
