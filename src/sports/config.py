from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NVIDIA NIM
    OPENAI_URL: str = "https://integrate.api.nvidia.com/v1"
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_ANON_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
