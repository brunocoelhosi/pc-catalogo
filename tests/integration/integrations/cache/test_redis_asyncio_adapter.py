import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import RedisDsn

from app.integrations.cache.redis_asyncio_adapter import RedisAsyncioAdapter


class TestRedisAsyncioAdapter:

    @pytest.fixture
    def redis_url(self):
        return RedisDsn("redis://localhost:6379/0")

    @pytest.fixture
    def mock_redis_client(self):
        mock = AsyncMock()
        return mock

    @pytest.fixture
    def redis_adapter(self, redis_url):
        with patch('redis.asyncio.Redis.from_url') as mock_from_url:
            mock_client = AsyncMock()
            mock_from_url.return_value = mock_client
            adapter = RedisAsyncioAdapter(redis_url)
            adapter.redis_client = mock_client
            return adapter

    def test_init(self, redis_url):
        """Testa inicialização do RedisAsyncioAdapter"""
        with patch('redis.asyncio.Redis.from_url') as mock_from_url:
            mock_client = AsyncMock()
            mock_from_url.return_value = mock_client
            
            # Act
            adapter = RedisAsyncioAdapter(redis_url)
            
            # Assert
            assert adapter.redis_url == str(redis_url)
            assert adapter.redis_client == mock_client
            mock_from_url.assert_called_once_with(str(redis_url))

    @pytest.mark.asyncio
    async def test_aclose(self, redis_adapter):
        """Testa fechamento da conexão Redis"""
        # Act
        await redis_adapter.aclose()
        
        # Assert
        redis_adapter.redis_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_exists_returns_true(self, redis_adapter):
        """Testa exists quando chave existe"""
        # Arrange
        redis_adapter.redis_client.exists.return_value = 1
        
        # Act
        result = await redis_adapter.exists("test_key")
        
        # Assert
        assert result is True
        redis_adapter.redis_client.exists.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_exists_returns_false(self, redis_adapter):
        """Testa exists quando chave não existe"""
        # Arrange
        redis_adapter.redis_client.exists.return_value = 0
        
        # Act
        result = await redis_adapter.exists("test_key")
        
        # Assert
        assert result is False
        redis_adapter.redis_client.exists.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_str_with_value(self, redis_adapter):
        """Testa get_str quando valor existe"""
        # Arrange
        redis_adapter.redis_client.get.return_value = b"test_value"
        
        # Act
        result = await redis_adapter.get_str("test_key")
        
        # Assert
        assert result == "test_value"
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_str_with_none(self, redis_adapter):
        """Testa get_str quando valor não existe"""
        # Arrange
        redis_adapter.redis_client.get.return_value = None
        
        # Act
        result = await redis_adapter.get_str("test_key")
        
        # Assert
        assert result is None
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_set_str_with_string_value(self, redis_adapter):
        """Testa set_str com valor string"""
        # Act
        await redis_adapter.set_str("test_key", "test_value")
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", "test_value", None)

    @pytest.mark.asyncio
    async def test_set_str_with_non_string_value(self, redis_adapter):
        """Testa set_str com valor não-string"""
        # Act
        await redis_adapter.set_str("test_key", 123)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", "123", None)

    @pytest.mark.asyncio
    async def test_set_str_with_expires(self, redis_adapter):
        """Testa set_str com tempo de expiração"""
        # Act
        await redis_adapter.set_str("test_key", "test_value", 300)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", "test_value", 300)

    @pytest.mark.asyncio
    async def test_set_str_with_none_value(self, redis_adapter):
        """Testa set_str com valor None (deve deletar)"""
        # Arrange
        redis_adapter.redis_client.delete = AsyncMock()
        
        # Act
        await redis_adapter.set_str("test_key", None)
        
        # Assert
        redis_adapter.redis_client.delete.assert_called_once_with("test_key")
        redis_adapter.redis_client.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_json_with_dict(self, redis_adapter):
        """Testa get_json com dicionário"""
        # Arrange
        test_dict = {"name": "João", "age": 30}
        redis_adapter.redis_client.get.return_value = json.dumps(test_dict).encode()
        
        # Act
        result = await redis_adapter.get_json("test_key")
        
        # Assert
        assert result == test_dict
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_json_with_list(self, redis_adapter):
        """Testa get_json com lista"""
        # Arrange
        test_list = [1, 2, 3, "test"]
        redis_adapter.redis_client.get.return_value = json.dumps(test_list).encode()
        
        # Act
        result = await redis_adapter.get_json("test_key")
        
        # Assert
        assert result == test_list
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_json_with_int(self, redis_adapter):
        """Testa get_json com inteiro"""
        # Arrange
        test_int = 42
        redis_adapter.redis_client.get.return_value = json.dumps(test_int).encode()
        
        # Act
        result = await redis_adapter.get_json("test_key")
        
        # Assert
        assert result == test_int
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_json_with_none(self, redis_adapter):
        """Testa get_json quando valor não existe"""
        # Arrange
        redis_adapter.redis_client.get.return_value = None
        
        # Act
        result = await redis_adapter.get_json("test_key")
        
        # Assert
        assert result is None
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_set_json_with_dict(self, redis_adapter):
        """Testa set_json com dicionário"""
        # Arrange
        test_dict = {"name": "João", "age": 30}
        redis_adapter.redis_client.set = AsyncMock()
        
        # Act
        await redis_adapter.set_json("test_key", test_dict)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", json.dumps(test_dict), None)

    @pytest.mark.asyncio
    async def test_set_json_with_list(self, redis_adapter):
        """Testa set_json com lista"""
        # Arrange
        test_list = [1, 2, 3, "test"]
        redis_adapter.redis_client.set = AsyncMock()
        
        # Act
        await redis_adapter.set_json("test_key", test_list)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", json.dumps(test_list), None)

    @pytest.mark.asyncio
    async def test_set_json_with_int(self, redis_adapter):
        """Testa set_json com inteiro"""
        # Arrange
        test_int = 42
        redis_adapter.redis_client.set = AsyncMock()
        
        # Act
        await redis_adapter.set_json("test_key", test_int)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", json.dumps(test_int), None)

    @pytest.mark.asyncio
    async def test_set_json_with_expires(self, redis_adapter):
        """Testa set_json com tempo de expiração"""
        # Arrange
        test_dict = {"name": "João"}
        redis_adapter.redis_client.set = AsyncMock()
        
        # Act
        await redis_adapter.set_json("test_key", test_dict, 300)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", json.dumps(test_dict), 300)

    @pytest.mark.asyncio
    async def test_set_json_with_none(self, redis_adapter):
        """Testa set_json com valor None"""
        # Arrange
        redis_adapter.redis_client.delete = AsyncMock()
        
        # Act
        await redis_adapter.set_json("test_key", None)
        
        # Assert
        redis_adapter.redis_client.delete.assert_called_once_with("test_key")
        redis_adapter.redis_client.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete(self, redis_adapter):
        """Testa delete de chave"""
        # Act
        await redis_adapter.delete("test_key")
        
        # Assert
        redis_adapter.redis_client.delete.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_json_with_invalid_json(self, redis_adapter):
        """Testa get_json com JSON inválido"""
        # Arrange
        redis_adapter.redis_client.get.return_value = b"invalid json"
        
        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            await redis_adapter.get_json("test_key")

    @pytest.mark.asyncio
    async def test_redis_url_conversion(self, redis_url):
        """Testa conversão da URL Redis"""
        with patch('redis.asyncio.Redis.from_url') as mock_from_url:
            mock_client = AsyncMock()
            mock_from_url.return_value = mock_client
            
            # Act
            adapter = RedisAsyncioAdapter(redis_url)
            
            # Assert
            assert isinstance(adapter.redis_url, str)
            assert adapter.redis_url == str(redis_url)

    @pytest.mark.asyncio
    async def test_set_str_with_boolean_value(self, redis_adapter):
        """Testa set_str com valor booleano"""
        # Act
        await redis_adapter.set_str("test_key", True)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", "True", None)

    @pytest.mark.asyncio
    async def test_set_str_with_float_value(self, redis_adapter):
        """Testa set_str com valor float"""
        # Act
        await redis_adapter.set_str("test_key", 3.14)
        
        # Assert
        redis_adapter.redis_client.set.assert_called_once_with("test_key", "3.14", None)

    @pytest.mark.asyncio
    async def test_get_str_with_empty_string(self, redis_adapter):
        """Testa get_str com string vazia"""
        # Arrange
        redis_adapter.redis_client.get.return_value = b""
        
        # Act
        result = await redis_adapter.get_str("test_key")
        
        # Assert
        assert result == ""
        redis_adapter.redis_client.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_exists_with_multiple_keys(self, redis_adapter):
        """Testa exists com múltiplas chaves (retorna count > 0)"""
        # Arrange
        redis_adapter.redis_client.exists.return_value = 3
        
        # Act
        result = await redis_adapter.exists("test_key")
        
        # Assert
        assert result is True