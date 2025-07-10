import pytest
import jwt
from unittest.mock import AsyncMock, MagicMock, patch
from app.integrations.auth.keycloak_adapter import (
    KeycloakAdapter,
    OAuthException,
    TokenExpiredException,
    InvalidTokenException
)


class TestKeycloakAdapter:

    @pytest.fixture
    def well_known_data(self):
        return {
            "authorization_endpoint": "http://keycloak:8080/realms/marketplace/protocol/openid-connect/auth",
            "jwks_uri": "http://keycloak:8080/realms/marketplace/protocol/openid-connect/certs"
        }

    @pytest.fixture
    def public_keys_data(self):
        return [
            {
                "kid": "test-kid-1",
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": "test-n-value",
                "e": "AQAB"
            },
            {
                "kid": "test-kid-2",
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "n": "test-n-value-2",
                "e": "AQAB"
            }
        ]

    @pytest.fixture
    def keycloak_adapter(self):
        return KeycloakAdapter("http://keycloak:8080/realms/marketplace/.well-known/openid-configuration")

    @pytest.fixture
    def mock_token(self):
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRlc3Qta2lkLTEifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.test-signature"

    @patch('httpx.Client')
    def test_load_well_known(self, mock_client, keycloak_adapter, well_known_data):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = well_known_data
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Act
        result = keycloak_adapter._load_well_known()

        # Assert
        assert result == well_known_data
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            "http://keycloak:8080/realms/marketplace/.well-known/openid-configuration"
        )

    def test_get_well_known_cached(self, keycloak_adapter, well_known_data):
        # Arrange
        keycloak_adapter._well_knwon = well_known_data

        # Act
        result = keycloak_adapter.get_well_knwon()

        # Assert
        assert result == well_known_data

    @patch('httpx.Client')
    def test_get_well_known_loads_if_none(self, mock_client, keycloak_adapter, well_known_data):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = well_known_data
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Act
        result = keycloak_adapter.get_well_knwon()

        # Assert
        assert result == well_known_data

    def test_get_authorization_endpoint(self, keycloak_adapter, well_known_data):
        # Arrange
        keycloak_adapter._well_knwon = well_known_data

        # Act
        result = keycloak_adapter.get_authorization_endpoint()

        # Assert
        assert result == "http://keycloak:8080/realms/marketplace/protocol/openid-connect/auth"

    """@pytest.mark.asyncio
    async def test_fetch_public_keys(self, keycloak_adapter, well_known_data, public_keys_data):
        # Arrange
        keycloak_adapter._well_knwon = well_known_data
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"keys": public_keys_data})  # AsyncMock para json()
            mock_response.raise_for_status = MagicMock()
            
            # Configurar o mock do context manager assíncrono
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await keycloak_adapter._fetch_public_keys()

            # Assert
            assert result == public_keys_data
            mock_client_instance.get.assert_called_once_with(
                "http://keycloak:8080/realms/marketplace/protocol/openid-connect/certs"
            )"""

    @pytest.mark.asyncio
    async def test_get_public_keys_cached(self, keycloak_adapter, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data

        # Act
        result = await keycloak_adapter.get_public_keys()

        # Assert
        assert result == public_keys_data

    """@pytest.mark.asyncio
    async def test_get_public_keys_fetch_if_none(self, keycloak_adapter, well_known_data, public_keys_data):
        # Arrange
        keycloak_adapter._well_knwon = well_known_data
        
        with patch('httpx.AsyncClient') as mock_async_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"keys": public_keys_data})  # AsyncMock para json()
            mock_response.raise_for_status = MagicMock()
            
            # Configurar o mock do context manager assíncrono
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance

            # Act
            result = await keycloak_adapter.get_public_keys()

            # Assert
            assert result == public_keys_data
"""
    def test_get_token_header(self, mock_token):
        # Act
        with patch('jwt.get_unverified_header') as mock_jwt:
            mock_jwt.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            result = KeycloakAdapter.get_token_header(mock_token)

            # Assert
            assert result == {"kid": "test-kid-1", "alg": "RS256"}
            mock_jwt.assert_called_once_with(mock_token)

    def test_get_header_info_from_token(self, mock_token):
        # Act
        with patch('jwt.get_unverified_header') as mock_jwt:
            mock_jwt.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            kid, alg = KeycloakAdapter.get_header_info_from_token(mock_token)

            # Assert
            assert kid == "test-kid-1"
            assert alg == "RS256"

    @pytest.mark.asyncio
    async def test_get_alg_key_for_kid_found(self, keycloak_adapter, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data

        # Act
        result = await keycloak_adapter.get_alg_key_for_kid("test-kid-1")

        # Assert
        assert result == public_keys_data[0]

    @pytest.mark.asyncio
    async def test_get_alg_key_for_kid_not_found(self, keycloak_adapter, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data

        # Act & Assert
        with pytest.raises(InvalidTokenException, match="Chave 'nonexistent-kid' não encontrada"):
            await keycloak_adapter.get_alg_key_for_kid("nonexistent-kid")

    @pytest.mark.asyncio
    async def test_validate_token_success(self, keycloak_adapter, mock_token, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data
        expected_payload = {"sub": "1234567890", "name": "John Doe", "admin": True}
        
        with patch('jwt.get_unverified_header') as mock_header, \
            patch('jwt.PyJWK') as mock_pyjwk, \
            patch('jwt.decode') as mock_decode:
            
            mock_header.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            mock_decode.return_value = expected_payload

            # Act
            result = await keycloak_adapter.validate_token(mock_token)

            # Assert
            assert result == expected_payload
            mock_decode.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_token_expired(self, keycloak_adapter, mock_token, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data
        
        with patch('jwt.get_unverified_header') as mock_header, \
            patch('jwt.PyJWK') as mock_pyjwk, \
            patch('jwt.decode') as mock_decode:
            
            mock_header.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            mock_decode.side_effect = jwt.ExpiredSignatureError("Token expired")

            # Act & Assert
            with pytest.raises(TokenExpiredException, match="Token expirou"):
                await keycloak_adapter.validate_token(mock_token)

    @pytest.mark.asyncio
    async def test_validate_token_invalid(self, keycloak_adapter, mock_token, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data
        
        with patch('jwt.get_unverified_header') as mock_header, \
            patch('jwt.PyJWK') as mock_pyjwk, \
            patch('jwt.decode') as mock_decode:
            
            mock_header.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            mock_decode.side_effect = jwt.InvalidTokenError("Invalid token")

            # Act & Assert
            with pytest.raises(InvalidTokenException, match="Token inválido"):
                await keycloak_adapter.validate_token(mock_token)

    @pytest.mark.asyncio
    async def test_validate_token_oauth_exception(self, keycloak_adapter, mock_token):
        # Arrange
        with patch.object(keycloak_adapter, 'get_header_info_from_token') as mock_header:
            mock_header.side_effect = InvalidTokenException("Header error")

            # Act & Assert
            with pytest.raises(InvalidTokenException, match="Header error"):
                await keycloak_adapter.validate_token(mock_token)

    @pytest.mark.asyncio
    async def test_validate_token_general_exception(self, keycloak_adapter, mock_token, public_keys_data):
        # Arrange
        keycloak_adapter._public_keys = public_keys_data
        
        with patch('jwt.get_unverified_header') as mock_header, \
            patch('jwt.PyJWK') as mock_pyjwk, \
            patch('jwt.decode') as mock_decode:
            
            mock_header.return_value = {"kid": "test-kid-1", "alg": "RS256"}
            mock_decode.side_effect = Exception("Unexpected error")

            # Act & Assert
            with pytest.raises(OAuthException, match="Falha ao validar o token"):
                await keycloak_adapter.validate_token(mock_token)


class TestExceptions:

    def test_oauth_exception(self):
        with pytest.raises(OAuthException):
            raise OAuthException("Test error")

    def test_token_expired_exception(self):
        with pytest.raises(TokenExpiredException):
            raise TokenExpiredException("Token expired")

    def test_invalid_token_exception(self):
        with pytest.raises(InvalidTokenException):
            raise InvalidTokenException("Invalid token")

    def test_exception_inheritance(self):
        assert issubclass(TokenExpiredException, OAuthException)
        assert issubclass(InvalidTokenException, OAuthException)