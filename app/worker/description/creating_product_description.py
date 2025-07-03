
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
            Analise os dados cadastrados do produto para nosso marketplace pelo seller.
            Você é uma especialista em marketplace. Gere uma descrição detalhada e atrativa para o produto abaixo, incluindo características técnicas, benefícios, aplicações e diferenciais. Use linguagem envolvente e profissional.

            A resposta sua DEVE ser um JSON válido, com no MÁXIMO 1000 caracteres, sem nenhum texto adicional antes ou depois.
            Exemplo de resposta:

            {{
            "description": "A Smart TV Samsung 4K 100 polegadas oferece imagens ultra nítidas, conectividade Wi-Fi, múltiplas entradas HDMI e design moderno. Ideal para quem busca qualidade e tecnologia de ponta em entretenimento doméstico."
            }}

            Segue aqui o produto cadastrado para analise:
            ---
            {catalogo}
            ---
            """
        payload = {"model": self.ia_model, "prompt": prompt, "stream": False, "format": "json"}

        try:
            logger.info(
                f"Enviando para análise da IA. Modelo: {self.ia_model}", extra={"Produto": catalogo}
            )
            async with httpx.AsyncClient(timeout=120) as http_client:
                response = await http_client.post(self.ia_api_url, json=payload)  
            # Lança um erro para respostas com código 4xx ou 5xx
            response.raise_for_status()

            # A resposta da API do Ollama com format: "json" já é um JSON
            response_data = response.json()

            # O conteúdo do JSON está na chave 'response'
            ia_response = json.loads(response_data["response"])

            logger.info(f"Análise da IA recebida: {ia_response}")
            
            logger.info(f"Resposta da IA: {ia_response}")
            return ia_response
        except httpx.HTTPError as e:
            logger.error(f"Erro ao chamar a API do Ollama: {e}", exc_info=True)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar a resposta JSON da IA: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado na função de análise da IA: {e}")