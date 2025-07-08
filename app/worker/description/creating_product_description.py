
from app.models.catalogo_model import CatalogoModel
import httpx
import json
from logging import getLogger
from app.settings import settings
logger = getLogger(__name__)

class CreatingProductDescription:
    def __init__(self, ia_api_url: str, ia_model: str):
        self.ia_model = ia_model
        self.ia_api_url = ia_api_url

    async def create_description(self, catalogo: CatalogoModel):
        
        """
        Vamos conversar com a IA, o texto seria bom carregar do banco!
        """

        prompt = f"""
        Você é um especialista em e-commerce. Crie uma descrição de produto em português baseada APENAS nos dados fornecidos abaixo.

        PRODUTO: {catalogo.name}

        INSTRUÇÕES:
        - Crie uma descrição profissional e atrativa para um produto de e-commerce
        - Use APENAS as informações do produto fornecido
        - Limite de até 300 caracteres
        - Retorne APENAS um JSON válido no formato exato abaixo
        - NÃO inclua texto adicional

        Formato de resposta:
        {{"description": "sua descrição aqui"}}
        """

        payload = {"model": self.ia_model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    
                    }

        try:
            logger.info(
                f"🤖Enviando para análise da IA. Modelo: {self.ia_model}", extra={"Produto": catalogo.name}
            )

            async with httpx.AsyncClient(timeout=200) as http_client:
                response = await http_client.post(self.ia_api_url, json=payload)  
            # Lança um erro para respostas com código 4xx ou 5xx
            response.raise_for_status()

            # A resposta da API do Ollama com format: "json" já é um JSON
            response_data = response.json()

            if "response" not in response_data:
                logger.error(f"❌ Chave 'response' não encontrada em: {response_data}")
                return None

            # O conteúdo do JSON está na chave 'response'
            ia_response = json.loads(response_data["response"])

            logger.info(f"Análise da IA recebida: {ia_response}")
            
            logger.info(f"Resposta da IA: {ia_response}")
            return ia_response
        
        except httpx.HTTPError as e:
            logger.error(f"❌ Erro HTTP: {e}", exc_info=True)
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro JSON decode: {e}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {type(e).__name__}: {e}")
            logger.error(f"❌ Traceback completo:", exc_info=True)
            return None