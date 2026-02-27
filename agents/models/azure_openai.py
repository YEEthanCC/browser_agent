from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.azure import AzureProvider
from configs.settings import Settings

settings = Settings()

azure_model = OpenAIModel(
    model_name="gpt-4o", 
    provider=AzureProvider(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        api_key=settings.AZURE_OPENAI_API_KEY,
    )
)