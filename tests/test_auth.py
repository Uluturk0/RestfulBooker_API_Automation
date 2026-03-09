from core.logger import logger

class TestAuth:
    """
    Authentication API Tests.
    Verifies token generation logic and security boundaries.
    """

    def test_create_token_success(self, auth_api):
        """
        Happy Path: Attempt to generate a token with valid, default admin credentials.
        Expected: 200 OK and a valid token string.
        """
        logger.info("Step 1: Requesting a new auth token with valid credentials.")
        response = auth_api.create_token()
        
        logger.info("Step 2: Validating response status code.")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        logger.info("Step 3: Verifying the presence and validity of the token.")
        assert "token" in response.json(), "Token key is missing in the response!"
        
        token_value = response.json()["token"]
        assert len(token_value) > 0, "Generated token is empty!"
        
        logger.info(f"Success! Token successfully retrieved: {token_value}")

    def test_create_token_invalid_credentials(self, auth_api):
        """
        Sad Path: Attempt to generate a token with a wrong password.
        Expected: In a good API, it should be 401 Unauthorized. 
        In Restful-Booker, it returns 200 with a "reason" key. We test the actual behavior.
        """
        logger.info("Step 1: Attempting login with invalid credentials (hacker_password_123).")
        response = auth_api.create_token(username="admin", password="hacker_password_123")
        
        logger.info("Step 2: Validating response status code (API returns 200 instead of 401).")
        assert response.status_code == 200
        
        logger.info("Step 3: Checking for the 'Bad credentials' error message in the payload.")
        response_data = response.json()
        
        assert "reason" in response_data, "Expected a 'reason' key for failed login!"
        assert response_data["reason"] == "Bad credentials", "Error message mismatch!"
        
        logger.info("Success! The API properly rejected the invalid credentials with a reason message.")