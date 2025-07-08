import pytest
import json
import httpx
from unittest.mock import AsyncMock, MagicMock, patch
from logging import getLogger

from app.worker.description.creating_product_description import CreatingProductDescription
from app.models.catalogo_model import CatalogoModel


class TestCreatingProductDescription:

    @pytest.fixture
    def ia_api_url(self):
        return "http://localhost:11434/api/generate"

    @pytest.fixture
    def ia_model(self):
        return "phi3"

    @pytest.fixture
    def creating_product_description(self, ia_api_url, ia_model):
        return CreatingProductDescription(ia_api_url, ia_model)

    @pytest.fixture
    def sample_catalogo(self):
        return CatalogoModel(
            seller_id="magalu",
            sku="TV123",
            name="Smart TV 55 polegadas 4K UHD"
        )

    @pytest.fixture
    def expected_prompt(self, sample_catalogo):
        return f"""
        Você é um especialista em e-commerce. Crie uma descrição de produto em português baseada APENAS nos dados fornecidos abaixo.

        PRODUTO: {sample_catalogo.name}

        INSTRUÇÕES:
        - Crie uma descrição atrativa e profissional
        - Use APENAS as informações do produto fornecido
        - Máximo 1000 caracteres
        - Retorne APENAS um JSON válido no formato exato abaixo
        - NÃO inclua texto adicional

        Formato de resposta:
        {{"description": "sua descrição aqui"}}
        """

    @pytest.fixture
    def mock_ia_response(self):
        return {
            "description": "Smart TV 55 polegadas com tecnologia 4K UHD para experiência visual incrível. Ideal para entretenimento doméstico."
        }

    @pytest.fixture
    def mock_ollama_response(self, mock_ia_response):
        return {
            "model": "phi3",
            "created_at": "2024-01-01T00:00:00Z",
            "response": json.dumps(mock_ia_response),
            "done": True
        }

    def test_init(self, ia_api_url, ia_model):
        """Testa inicialização da classe CreatingProductDescription"""
        # Act
        instance = CreatingProductDescription(ia_api_url, ia_model)
        
        # Assert
        assert instance.ia_api_url == ia_api_url
        assert instance.ia_model == ia_model

    @pytest.mark.asyncio
    async def test_create_description_success(
        self,
        creating_product_description,
        sample_catalogo,
        mock_ollama_response,
        mock_ia_response,
        expected_prompt
    ):
        """Testa criação de descrição com sucesso"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_ollama_response)
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result == mock_ia_response
            mock_client_instance.post.assert_called_once_with(
                creating_product_description.ia_api_url,
                json={
                    "model": creating_product_description.ia_model,
                    "prompt": expected_prompt,
                    "stream": False,
                    "format": "json"
                }
            )

    @pytest.mark.asyncio
    async def test_create_description_http_error(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa tratamento de erro HTTP"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.HTTPError("Connection failed")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result is None
            mock_logger.error.assert_called_once()
            assert "Erro ao chamar a API do Ollama" in str(mock_logger.error.call_args)

    @pytest.mark.asyncio
    async def test_create_description_http_status_error(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa tratamento de erro de status HTTP"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:
        
            mock_client_instance = AsyncMock()
            # Configure o mock para lançar erro no post, não no raise_for_status
            mock_client_instance.post.side_effect = httpx.HTTPStatusError(
                "400 Bad Request", 
                request=MagicMock(), 
                response=MagicMock()
            )
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result is None
            mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_description_json_decode_error_in_ollama_response(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa tratamento de erro de decode JSON na resposta do Ollama"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:
            
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(side_effect=json.JSONDecodeError("Invalid JSON", "", 0))  # Corrigido
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result is None
            mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_description_json_decode_error_in_ia_response(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa tratamento de erro de decode JSON na resposta da IA"""
        # Arrange
        mock_ollama_response = {
            "response": "invalid json response"  # JSON inválido na resposta da IA
        }
        
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:
            
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_ollama_response)  # Corrigido
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result is None
            mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_description_unexpected_error(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa tratamento de erro inesperado"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = Exception("Unexpected error")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert result is None
            mock_logger.error.assert_called_once()
            assert "Erro inesperado na função de análise da IA" in str(mock_logger.error.call_args)

    @pytest.mark.asyncio
    async def test_create_description_with_different_product(self, creating_product_description):
        """Testa criação de descrição com produto diferente"""
        # Arrange
        catalogo = CatalogoModel(
            seller_id="amazon",
            sku="BOOK456", 
            name="Livro de Programação Python"
        )
        
        mock_ia_response = {
            "description": "Livro completo sobre programação Python para iniciantes e avançados."
        }
        
        mock_ollama_response = {
            "response": json.dumps(mock_ia_response)
        }
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_ollama_response)
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(catalogo)

            # Assert
            assert result == mock_ia_response

    @pytest.mark.asyncio
    async def test_create_description_timeout_configuration(
        self, 
        creating_product_description, 
        sample_catalogo
    ):
        """Testa se o timeout está configurado corretamente"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"response": '{"description": "test"}'})  # Corrigido
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            await creating_product_description.create_description(sample_catalogo)

            # Assert
            mock_async_client.assert_called_once_with(timeout=120)

    @pytest.mark.asyncio
    async def test_create_description_payload_format(
        self, 
        creating_product_description, 
        sample_catalogo,
        expected_prompt
    ):
        """Testa se o payload está no formato correto"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"response": '{"description": "test"}'})  # Corrigido
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            await creating_product_description.create_description(sample_catalogo)

            # Assert
            call_args = mock_client_instance.post.call_args
            payload = call_args[1]['json']
            
            assert payload['model'] == creating_product_description.ia_model
            assert payload['prompt'] == expected_prompt
            assert payload['stream'] is False
            assert payload['format'] == "json"

    @pytest.mark.asyncio
    async def test_create_description_logging(
        self, 
        creating_product_description, 
        sample_catalogo,
        mock_ollama_response,
        mock_ia_response
    ):
        """Testa se os logs estão sendo gerados corretamente"""
        # Arrange
        with patch('httpx.AsyncClient') as mock_async_client, \
            patch('app.worker.description.creating_product_description.logger') as mock_logger:  # Corrigido
        
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_ollama_response)  # Corrigido
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            await creating_product_description.create_description(sample_catalogo)

            # Assert
            assert mock_logger.info.call_count == 3
            
            # Verifica os logs chamados
            call_args_list = [call[0][0] for call in mock_logger.info.call_args_list]
            assert any("Enviando para análise da IA" in log for log in call_args_list)
            assert any("Análise da IA recebida" in log for log in call_args_list)
            assert any("Resposta da IA" in log for log in call_args_list)

    @pytest.mark.asyncio
    async def test_debug_create_description(
        self,
        creating_product_description,
        sample_catalogo,
        mock_ollama_response
    ):
        """Teste de debug para verificar o comportamento"""
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_ollama_response)  # Corrigido: usar AsyncMock
            mock_response.raise_for_status = MagicMock()

            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await creating_product_description.create_description(sample_catalogo)

            # Debug
            print(f"Result: {result}")
            print(f"Mock response called: {mock_response.json.called}")
            print(f"Mock post called: {mock_client_instance.post.called}")
            
            # Assert básico
            assert result is not None