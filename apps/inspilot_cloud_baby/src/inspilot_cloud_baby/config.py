from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BUSINESS_ROBOT_", env_file=".env")

    database_url: str = "postgresql+psycopg://inspilot_cloud_baby:inspilot_cloud_baby@localhost:5432/inspilot_cloud_baby"
    attachment_root: Path = Path("./var/attachments")
    dws_binary: str = "dws"


settings = Settings()
