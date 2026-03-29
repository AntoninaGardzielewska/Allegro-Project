import os

from dotenv import load_dotenv

load_dotenv()


class AllegroAuthClient:
    def __init__(self):
        self._token = None
        self._expires_at = None
        self.client_id = os.getenv("OAUTH_CLIENT_ID")
        self.client_secret = os.getenv("OAUTH_CLIENT_SECRET")

    def get_device_code(self):
        pass

    def poll_for_token(self, device_code: str):
        pass

    def _refresh_token(self):
        pass

    def get_valid_token(self):
        pass
