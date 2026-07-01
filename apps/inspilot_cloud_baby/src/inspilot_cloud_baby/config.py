from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BUSINESS_ROBOT_", env_file=".env")

    database_url: str = "postgresql+psycopg://inspilot_cloud_baby:inspilot_cloud_baby@localhost:5432/inspilot_cloud_baby"
    attachment_root: Path = Path("./var/attachments")
    # DingTalk enterprise internal app credentials (AppKey/AppSecret) — enables
    # admin-level API access (can query ALL approval instances org-wide).
    dingtalk_app_key: str = ""      # DingTalk AppKey
    dingtalk_app_secret: str = ""   # DingTalk AppSecret

    # OpenAI Embedding 配置
    openai_api_key: str = ""  # BUSINESS_ROBOT_OPENAI_API_KEY
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimensions: int = 1536
    openai_base_url: str = ""  # 可选，支持代理或兼容 API

    # 向量检索开关
    enable_vector_search: bool = True

    # 对话模型配置（OpenAI 兼容；OpenRouter / DeepSeek / OpenAI 均可）
    chat_api_key: str = ""       # BUSINESS_ROBOT_CHAT_API_KEY
    chat_base_url: str = ""      # BUSINESS_ROBOT_CHAT_BASE_URL，如 https://openrouter.ai/api/v1
    chat_model: str = ""         # BUSINESS_ROBOT_CHAT_MODEL，如 openai/gpt-4o-mini

    # 生产库通道按需触发开关：开启时，仅当问题命中实时数据信号（订单/费率/编号等）
    # 才生成并执行 SQL，避免纯知识库问题白付一次 SQL 生成 LLM 调用 + SQL Server 往返。
    # 关闭则恢复"双通道无脑全跑"的原始行为。
    enable_prod_db_gate: bool = True

    # Rerank（重排）配置 — OpenAI 兼容的 /rerank 端点（Jina / Cohere / SiliconFlow 等）。
    # 向量召回后用 cross-encoder 精排，显著提升 top-k 相关性。无 key 时自动降级跳过。
    rerank_api_key: str = ""     # BUSINESS_ROBOT_RERANK_API_KEY
    rerank_base_url: str = ""    # BUSINESS_ROBOT_RERANK_BASE_URL，如 https://api.siliconflow.cn/v1
    rerank_model: str = ""       # BUSINESS_ROBOT_RERANK_MODEL，如 BAAI/bge-reranker-v2-m3
    enable_rerank: bool = True   # 有配置才生效

    # 检索增强开关
    enable_hybrid_search: bool = True   # 关键词(jieba)+向量 RRF 混合检索
    enable_query_rewrite: bool = False  # LLM 查询改写（多一次 LLM 调用，增加延迟，默认关）

    # 生产数据库配置（SQL Server，只读连接）
    prod_db_host: str = ""       # BUSINESS_ROBOT_PROD_DB_HOST
    prod_db_port: int = 1433     # BUSINESS_ROBOT_PROD_DB_PORT
    prod_db_name: str = ""       # BUSINESS_ROBOT_PROD_DB_NAME
    prod_db_user: str = ""       # BUSINESS_ROBOT_PROD_DB_USER
    prod_db_password: str = ""   # BUSINESS_ROBOT_PROD_DB_PASSWORD


settings = Settings()
