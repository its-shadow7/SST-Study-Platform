import base64
import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

class Settings:
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", os.getenv("VERCEL_ENV", "development")).strip().lower()

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    GOOGLE_ALLOWED_HD: str = os.getenv("GOOGLE_ALLOWED_HD", "sst.scaler.com").strip()
    ALLOW_DEV_MOCK_LOGIN: bool = os.getenv("ALLOW_DEV_MOCK_LOGIN", "false").lower() in ("true", "1")
    SPECIAL_EMAILS: str = os.getenv("SPECIAL_EMAILS", "").strip()
    
    # JWT Asymmetric Keys (RS256)
    JWT_PRIVATE_KEY_B64: str = os.getenv("JWT_PRIVATE_KEY_B64", "").strip()
    JWT_PUBLIC_KEY_B64: str = os.getenv("JWT_PUBLIC_KEY_B64", "").strip()
    
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "sst-study-platform").strip()
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "sst-students").strip()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "").strip()
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "sst_study").strip()
    
    # Upstash Redis
    UPSTASH_REDIS_REST_URL: str = os.getenv("UPSTASH_REDIS_REST_URL", "").strip()
    UPSTASH_REDIS_REST_TOKEN: str = os.getenv("UPSTASH_REDIS_REST_TOKEN", "").strip()
    
    # OpenAI Moderation
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
    
    # Rate Limiting Thresholds (Configurable via environment)
    RATE_LIMIT_NONCE_MAX: int = int(os.getenv("RATE_LIMIT_NONCE_MAX", "60"))
    RATE_LIMIT_NONCE_WINDOW: int = int(os.getenv("RATE_LIMIT_NONCE_WINDOW", "60"))
    RATE_LIMIT_LOGIN_MAX: int = int(os.getenv("RATE_LIMIT_LOGIN_MAX", "15"))
    RATE_LIMIT_LOGIN_WINDOW: int = int(os.getenv("RATE_LIMIT_LOGIN_WINDOW", "60"))
    RATE_LIMIT_REFRESH_MAX: int = int(os.getenv("RATE_LIMIT_REFRESH_MAX", "30"))
    RATE_LIMIT_REFRESH_WINDOW: int = int(os.getenv("RATE_LIMIT_REFRESH_WINDOW", "60"))
    RATE_LIMIT_COMMENT_MAX: int = int(os.getenv("RATE_LIMIT_COMMENT_MAX", "10"))
    RATE_LIMIT_COMMENT_WINDOW: int = int(os.getenv("RATE_LIMIT_COMMENT_WINDOW", "60"))
    
    # Auto-quarantine thresholds
    AUTO_QUARANTINE_REPORT_THRESHOLD: int = int(os.getenv("AUTO_QUARANTINE_REPORT_THRESHOLD", "5"))
    AUTO_QUARANTINE_WINDOW_HOURS: int = int(os.getenv("AUTO_QUARANTINE_WINDOW_HOURS", "2"))
    
    # Origin & Cookies
    APP_ORIGIN: str = os.getenv("APP_ORIGIN", "http://localhost:5173").strip()
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() in ("true", "1")
    COOKIE_SAMESITE: str = "strict"

    def get_private_key_pem(self) -> Optional[bytes]:
        if not self.JWT_PRIVATE_KEY_B64:
            return None
        return base64.b64decode(self.JWT_PRIVATE_KEY_B64)

    def get_public_key_pem(self) -> Optional[bytes]:
        if not self.JWT_PUBLIC_KEY_B64:
            return None
        return base64.b64decode(self.JWT_PUBLIC_KEY_B64)

settings = Settings()

def get_settings() -> Settings:
    return settings

