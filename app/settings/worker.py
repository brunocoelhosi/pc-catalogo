from pydantic import Field

from .app import AppSettings

class WorkerSettings(AppSettings):
    
    number_workers: int = Field(1)

    #ia_api_url: str = Field("https://localhost:11434/api/generate", description="URL da IA")
    ia_api_url: str = Field("http://ollama:11434/api/generate", description="URL da IA")
    # Alterado para um modelo menor e mais confiável devido a problemas de timeout de rede com phi3
    ia_model: str = Field("phi3", description="Modelo da IA")

worker_settings = WorkerSettings()

