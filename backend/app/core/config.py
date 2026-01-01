# Corrected config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Architectural Design Assistant"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./architect.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-min-32-chars-required")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")

    # 🔥 Added
    LLM_MODE: str = os.getenv("LLM_MODE", "mock")
    EMBEDDING_MODE: str = os.getenv("EMBEDDING_MODE", "mock")

    AI_MODEL: str = "gpt-4o-mini"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 800

    # CORS - can be comma-separated string or list
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"
    
    def get_cors_origins(self) -> list:
        """Parse CORS origins from string or return as list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Create settings instance **after class definition**
settings = Settings()
