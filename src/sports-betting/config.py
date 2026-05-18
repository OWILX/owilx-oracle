from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NVIDIA NIM
    NIM_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NIM_API_KEY: str
    NIM_MODEL_NAME: str = "meta/llama3-70b-instruct"   # placeholder – you'll change

    # API-Football
    APIFOOTBALL_KEY: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
