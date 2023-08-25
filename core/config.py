from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Settings(BaseSettings):
    MONGODB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TOKEN_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    REDIS_HOST: str
    THROTTLE: int
    LIMIT_CALL_PER_HOUR: int
    LIMIT_BAD_CALL_PER_HOUR: int
    FILES_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()
