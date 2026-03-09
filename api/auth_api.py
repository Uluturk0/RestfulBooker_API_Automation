from core.base_client import BaseClient
from core.config import Config

class AuthAPI(BaseClient):
    """
    API client for handling Authentication.
    Generates the token required for protected endpoints (PUT, PATCH, DELETE).
    """

    def create_token(self, username: str = Config.ADMIN_USERNAME, password: str = Config.ADMIN_PASSWORD):
        """
        Sends credentials to the /auth endpoint to receive a token.
        If no arguments are provided, it automatically uses the .env credentials.
        """
        payload = {
            "username": username,
            "password": password
        }
        
        return self.post("/auth", payload=payload)