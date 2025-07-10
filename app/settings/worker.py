from pydantic import Field

from .app import AppSettings

class WorkerSettings(AppSettings):
    
    number_workers: int = Field(1)
    ia_api_url: str = Field("http://ollama:11434/api/generate", description="URL da IA") 
    ia_model: str = Field("phi3", description="Modelo da IA")

worker_settings = WorkerSettings()

