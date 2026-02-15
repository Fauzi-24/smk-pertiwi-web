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
    "*", 
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

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str
    admin_key: str = "prismoji"
    
    # Server Config
    port: int = 8000
    frontend_url: str = "http://localhost:5173"
    app_name: str = "SMK Pertiwi Chatbot"
    
    # Gemini Config
    gemini_model: str = "gemini-1.5-flash"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    # Web Search
    enable_web_search: bool = True
    auto_web_search: bool = False
    web_search_results: int = 5
    web_search_cache_ttl: int = 1800
    web_search_cache_max: int = 120
    
    # Rate Limiting
    rate_limit_per_min: int = 30
    rate_limit_window: int = 60
    min_request_interval: float = 1.2
    
    # Moderation
    moderation_enabled: bool = True
    moderation_blocklist: str = "anjing,babi,bangsat,brengsek,kontol,memek,ngentot,goblok,tolol,fuck,shit"
    
    # SerpAPI
    serpapi_api_key: str = ""
    serpapi_engine: str = "google"
    serpapi_hl: str = "id"
    serpapi_gl: str = "id"
    
    # Email Configuration
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = "ozieefauzi599@gmail.com"
    email_password: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields in .env without error
        env_file_encoding = "utf-8"

    @property
    def cors_allow_origins(self) -> List[str]:
        # The cors_origins field was removed in the new Settings class definition.
        # This property now needs to be adapted or removed if it's no longer relevant.
        # Assuming it should now just return the default origins plus the frontend_url.
        origins = list(DEFAULT_CORS_ORIGINS)
        if self.frontend_url and self.frontend_url not in origins:
            origins.append(self.frontend_url)
        return origins


settings = Settings()
