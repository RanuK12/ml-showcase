from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "MySaaS"
    app_env: str = "development"
    secret_key: str
    backend_cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id_monthly: str = ""
    stripe_price_id_yearly: str = ""

    # Email
    resend_api_key: str = ""
    email_from: str = "noreply@example.com"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
