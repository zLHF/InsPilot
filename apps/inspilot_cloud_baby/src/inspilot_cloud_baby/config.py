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

    # 生产数据库配置（SQL Server，只读连接）
    prod_db_host: str = ""       # BUSINESS_ROBOT_PROD_DB_HOST
    prod_db_port: int = 1433     # BUSINESS_ROBOT_PROD_DB_PORT
    prod_db_name: str = ""       # BUSINESS_ROBOT_PROD_DB_NAME
    prod_db_user: str = ""       # BUSINESS_ROBOT_PROD_DB_USER
    prod_db_password: str = ""   # BUSINESS_ROBOT_PROD_DB_PASSWORD


settings = Settings()
