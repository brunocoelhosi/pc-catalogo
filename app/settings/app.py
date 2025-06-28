from pydantic import Field, HttpUrl, MongoDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carregar antes da definição
load_dotenv()

class AppSettings(BaseSettings):
    version: str = "0.0.2"

    app_name: str = Field(default="Catálogo API", title="Nome da aplicação")

    app_db_url_mongo: MongoDsn = Field(..., title="URI para o MongoDB")

    app_openid_wellknown: HttpUrl = Field(..., title="URL para well known de um openid")

    # XXX Configurações para o logging.
    pc_logging_level: str = Field("WARNING", description="Nível do logging")
    pc_logging_env: str = Field("prod", description="Ambiente do logging (prod ou dev ou test)")
    
settings = AppSettings()
