import pytest
import respx
import time
from httpx import Response
from allegro_project.auth.client import AllegroAuthClient
from allegro_project.config import Settings

@pytest.fixture
def mock_settings():
    return Settings(allegro_client_auth="test_id", allegro_client_secret="test_secret")

@pytest.mark.asyncio
@respx.mock
async def test_get_valid_token_new_flow(mock_settings):
    client = AllegroAuthClient(mock_settings)
    
    # 1. Mock Device Code Response
    respx.post("https://allegro.pl/auth/oauth/device").mock(return_value=Response(200, json={
        "device_code": "dev_123",
        "user_code": "ABC-DEF",
        "verification_uri": "https://allegro.pl/auth/activate",
        "expires_in": 300,
        "interval": 5
    }))

    # 2. Mock Token Polling (Success)
    respx.post("https://allegro.pl/auth/oauth/token").mock(return_value=Response(200, json={
        "access_token": "access_123",
        "refresh_token": "refresh_123",
        "expires_in": 3600,
        "token_type": "bearer"
    }))

    token = await client.get_valid_token()
    
    assert token == "access_123"
    assert client._refresh_token == "refresh_123"
    await client.aclose()

@pytest.mark.asyncio
@respx.mock
async def test_refresh_token_logic(mock_settings):
    client = AllegroAuthClient(mock_settings)
    # Manually set an expired state
    client._refresh_token = "old_refresh"
    client._expires_at = time.time() - 100 
    
    respx.post("https://allegro.pl/auth/oauth/token").mock(return_value=Response(200, json={
        "access_token": "new_access",
        "refresh_token": "new_refresh",
        "expires_in": 3600
    }))

    token = await client.get_valid_token()
    assert token == "new_access"
    assert respx.calls.last.request.read().decode() == "grant_type=refresh_token&refresh_token=old_refresh"
    await client.aclose()