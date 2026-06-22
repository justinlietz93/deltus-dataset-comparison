from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    export_root: str
    sqlserver_dsn: str | None


def load_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "local"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./runs/comparison_evidence.db"),
        export_root=os.getenv("EXPORT_ROOT", "./exports"),
        sqlserver_dsn=os.getenv("SQLSERVER_DSN") or None,
    )
