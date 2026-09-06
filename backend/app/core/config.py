import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/lingualead"))
    VAPI_API_KEY: str = Field(default_factory=lambda: os.getenv("VAPI_API_KEY", ""))
    VAPI_ASSISTANT_ID: str = Field(default_factory=lambda: os.getenv("VAPI_ASSISTANT_ID", ""))
    VAPI_PHONE_NUMBER_ID: str = Field(default_factory=lambda: os.getenv("VAPI_PHONE_NUMBER_ID", ""))
    VAPI_WEBHOOK_SECRET: str = Field(default_factory=lambda: os.getenv("VAPI_WEBHOOK_SECRET", ""))
    TWILIO_ACCOUNT_SID: str = Field(default_factory=lambda: os.getenv("TWILIO_ACCOUNT_SID", ""))
    TWILIO_AUTH_TOKEN: str = Field(default_factory=lambda: os.getenv("TWILIO_AUTH_TOKEN", ""))
    GROQ_API_KEY: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    ENVIRONMENT: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    PORT: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env")),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
