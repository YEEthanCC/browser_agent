from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    URI: str
    AZURE_AI_PROJECT_ENDPOINT: str
    AZURE_AI_PROJECT_API_KEY: str
    APPLICATIONINSIGHTS_CONNECTION_STRING: str

    class Config:
        env_file = ".env"
        env_prefix: str = ""