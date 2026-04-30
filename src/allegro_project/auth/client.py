import asyncio
import logging
import time
from typing import Optional

import httpx

from allegro_project.auth.models import DeviceCodeResponse, TokenResponse
from allegro_project.config import Settings

logger = logging.getLogger(__name__)


class AllegroAuthClient:
    TIME_BUFFER = 10
    TRY_POLL_X_TIMES = 100
    BASE_URL = "https://allegro.pl"

    def __init__(self, settings: Settings):
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expires_at: float = 0
        self._device_code: Optional[str] = None
        self._client_id: str = settings.allegro_client_auth
        self._client_secret: str = settings.allegro_client_secret

        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL, auth=(self._client_id, self._client_secret)
        )

    @property
    def _is_expired(self) -> bool:
        return time.time() > (self._expires_at - self.TIME_BUFFER)

    async def aclose(self):
        """Closes the underlying HTTP client."""
        await self._client.aclose()

    def _update_tokens(self, token: TokenResponse):
        self._access_token = token.access_token
        self._refresh_token = token.refresh_token
        self._expires_at = time.time() + token.expires_in
        logger.info("Tokens updated successfully")

    async def _get_device_code(self) -> None:
        response = await self._client.post("/auth/oauth/device")
        response.raise_for_status()

        data = DeviceCodeResponse(**response.json())
        self._device_code = data.device_code
        logger.info(
            "Visit %s and enter code: %s",
            data.verification_uri,
            data.user_code,
        )

    async def _poll_for_token(self, max_tries: int = 100, interval: int = 5) -> None:
        for _ in range(max_tries):
            response = await self._client.post(
                "/auth/oauth/token",
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": self._device_code,
                },
            )
            if response.status_code == 200:
                self._update_tokens(TokenResponse(**response.json()))
                return

            await asyncio.sleep(interval)

        raise TimeoutError("User did not approve the device in time")

    async def _refresh_access_token(self) -> None:
        response = await self._client.post(
            "auth/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            },
        )
        response.raise_for_status()
        self._update_tokens(TokenResponse(**response.json()))

    async def get_valid_token(self) -> str | None:
        if self._is_expired:
            if self._refresh_token is None:
                await self._get_device_code()
                await self._poll_for_token()
            else:
                try:
                    await self._refresh_access_token()
                except httpx.HTTPStatusError:
                    # If refresh fails (e.g. revoked), restart device flow
                    logger.warning("Refresh token invalid, restarting device flow.")
                    await self._get_device_code()
                    await self._poll_for_token()
        return self._access_token
