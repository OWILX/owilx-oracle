from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NVIDIA NIM
    LLM_URL: str = "https://integrate.api.nvidia.com/v1"
    LLM_API_KEY: str
    LLM_NAME: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_ANON_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
