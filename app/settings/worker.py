from pydantic import Field

from .app import AppSettings


"""class WorkerSettings(AppSettings):
    enabled_workers: set[str] = Field(
        default={"customer"},
        title="Workers que devem ser inicializados",
    )"""

class WorkerSettings(AppSettings):
    
    number_workers: int = Field(1)

    ia_api_url: str = Field("http://localhost:11434/api/generate", description="URL da IA")
    #ia_model: str = Field("llama3:8b", description="Modelo da IA")
    ia_model: str = Field("phi3", description="Modelo da IA")

worker_settings = WorkerSettings()

