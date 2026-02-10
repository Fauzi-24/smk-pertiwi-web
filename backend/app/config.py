from typing import List, Optional
from pydantic_settings import BaseSettings # type: ignore
from pydantic import Field, SecretStr

DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

class Settings(BaseSettings):
    # API Configuration
    gemini_api_key: Optional[SecretStr] = Field(None, env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-2.5-flash", env="GEMINI_MODEL")
    max_tokens: int = Field(1000, env="MAX_TOKENS")
    temperature: float = Field(0.7, env="TEMPERATURE")

    # Server Configuration
    port: int = Field(8000, env="PORT")
    frontend_url: str = Field("http://localhost:5173", env="FRONTEND_URL")
    app_name: str = Field("SMK Pertiwi Chatbot", env="APP_NAME")

    # CORS Origins (comma-separated)
    cors_origins: Optional[str] = Field(None, env="CORS_ORIGINS")

    # Web Search Configuration
    enable_web_search: bool = Field(False, env="ENABLE_WEB_SEARCH")
    auto_web_search: bool = Field(False, env="AUTO_WEB_SEARCH")
    web_search_results: int = Field(5, env="WEB_SEARCH_RESULTS")
    web_search_cache_ttl: int = Field(1800, env="WEB_SEARCH_CACHE_TTL")
    web_search_cache_max: int = Field(120, env="WEB_SEARCH_CACHE_MAX")
    serpapi_api_key: Optional[SecretStr] = Field(None, env="SERPAPI_API_KEY")
    serpapi_engine: str = Field("google", env="SERPAPI_ENGINE")
    serpapi_hl: str = Field("id", env="SERPAPI_HL")
    serpapi_gl: str = Field("id", env="SERPAPI_GL")

    # Rate Limit Configuration
    rate_limit_per_min: int = Field(30, env="RATE_LIMIT_PER_MIN")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")
    min_request_interval: float = Field(1.2, env="MIN_REQUEST_INTERVAL")

    # Moderation Configuration
    moderation_enabled: bool = Field(True, env="MODERATION_ENABLED")
    moderation_blocklist: str = Field(
        "anjing,babi,bangsat,brengsek,kontol,memek,ngentot,goblok,tolol,fuck,shit",
        env="MODERATION_BLOCKLIST"
    )

    # Admin Configuration
    admin_key: Optional[SecretStr] = Field(None, env="ADMIN_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_allow_origins(self) -> List[str]:
        if self.cors_origins:
            items = [item.strip() for item in self.cors_origins.split(",") if item.strip()]
            return items
        origins = list(DEFAULT_CORS_ORIGINS)
        if self.frontend_url and self.frontend_url not in origins:
            origins.append(self.frontend_url)
        return origins


settings = Settings()
