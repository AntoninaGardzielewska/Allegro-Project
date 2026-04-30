import logging
import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class AllegroAuthClient:
    TIME_BUFFER = 10
    TRY_POLL_X_TIMES = 100
    REQUIRED_TOKEN_FIELDS = ["access_token", "refresh_token", "expires_in"]

    def __init__(self):
        self._access_token = None
        self._refresh_token = None
        self._expires_at = time.time()
        self._device_code = None

        client_id = os.getenv("OAUTH_CLIENT_ID")
        client_secret = os.getenv("OAUTH_CLIENT_SECRET")

        if not client_id:
            raise ValueError("OAUTH_CLIENT_ID environment variable is not set")
        if not client_secret:
            raise ValueError("OAUTH_CLIENT_SECRET environment variable is not set")

        self._client_id: str = client_id
        self._client_secret: str = client_secret

    def _get_device_code(self) -> None:
        response = httpx.post(
            "https://allegro.pl/auth/oauth/device",
            auth=(self._client_id, self._client_secret),
        )
        data = response.json()
        if "device_code" not in data:
            raise ValueError(f"Unexpected response from Allegro: {data}")

        self._device_code = data["device_code"]
        logger.info(
            "Visit %s and enter code: %s",
            data.get("verification_uri", "https://allegro.pl/device"),
            data.get("user_code", ""),
        )

    def _poll_for_token(self) -> None:
        try_x_times = self.TRY_POLL_X_TIMES
        while True:
            response = httpx.post(
                "https://allegro.pl/auth/oauth/token",
                auth=(self._client_id, self._client_secret),
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": self._device_code,
                },
            )
            if response.status_code == 200:
                data = response.json()
                if not all(key in data for key in self.REQUIRED_TOKEN_FIELDS):
                    raise ValueError(f"Unexpected response from Allegro: {data}")

                self._access_token = data["access_token"]
                self._refresh_token = data["refresh_token"]
                self._expires_at = time.time() + data["expires_in"]
                logger.info("Access token received")
                return

            try_x_times -= 1
            if try_x_times == 0:
                logger.error(
                    "Polling timed out — user did not approve the device in time"
                )
                raise TimeoutError("User did not approve the device in time")
            time.sleep(5)

    def _run_refresh_token(self) -> None:
        response = httpx.post(
            "https://allegro.pl/auth/oauth/token",
            auth=(self._client_id, self._client_secret),
            data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            },
        )
        if response.status_code == 200:
            data = response.json()
            if not all(key in data for key in self.REQUIRED_TOKEN_FIELDS):
                raise ValueError(f"Unexpected response from Allegro: {data}")

            self._access_token = data["access_token"]
            self._refresh_token = data["refresh_token"]
            self._expires_at = time.time() + data["expires_in"]
            logger.info("Token refreshed successfully")
        else:
            logger.error(
                "Failed to refresh token: %s %s", response.status_code, response.text
            )
            raise httpx.HTTPError("Failed to refresh token")

    def get_valid_token(self) -> str | None:
        if self._expires_at - self.TIME_BUFFER < time.time():
            if self._refresh_token is None:
                self._get_device_code()
                self._poll_for_token()
            else:
                self._run_refresh_token()
        return self._access_token
