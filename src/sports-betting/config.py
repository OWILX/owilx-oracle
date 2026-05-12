import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str   # for admin operations (table creation, etc.)
    SUPABASE_ANON_KEY: str      # for public API (RLS allowed)

    # API-Football
    APIFOOTBALL_KEY: str
    APIFOOTBALL_BASE_URL: str = "https://v3.football.api-sports.io"

    # NVIDIA NIM
    NIM_BASE_URL: str
    NIM_API_KEY: str
    NIM_MODEL_NAME: str = "hermes-3-llama-3.2-3b"  # or "deepseek-ai/deepseek-coder-6.7b-instruct"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
