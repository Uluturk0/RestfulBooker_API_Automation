import pytest
import json
import os
from core.logger import logger
from utils.data_generator import generate_random_booking_payload

def load_boundary_payloads():
    """
    Helper function to load boundary/malicious payloads from a JSON file.
    Returns a list of payload dictionaries to be used in parameterized tests.
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'test_data', 'payloads.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["boundary_payloads"]

class TestNegativeBooking:
    """
    Sad Path (Negative) Test Suite.
    We intentionally break the rules to ensure the API's defense mechanisms work.
    """

    def test_delete_booking_without_valid_token(self, booking_api):
        """
        Attempt to delete a booking using an invalid token.
        Expected: 403 Forbidden
        """
        fake_id = 1 
        invalid_token = "im_a_hacker_123"
        
        logger.info(f"Step 1: Attempting to delete booking ID {fake_id} with an invalid token.")
        response = booking_api.delete_booking(booking_id=fake_id, token=invalid_token)
        
        logger.info(f"Step 2: Validating that the API blocks the request with 403 Forbidden.")
        assert response.status_code == 403, f"Security Breach! Expected 403, but got {response.status_code}"
        logger.info("Success: API properly rejected the unauthorized deletion attempt.")

    def test_get_non_existent_booking(self, booking_api):
        """
        Attempt to read a booking ID that does not exist.
        Expected: 404 Not Found
        """
        absurd_id = 99999999999999  # An ID that will never exist
        
        logger.info(f"Step 1: Requesting a non-existent booking ID: {absurd_id}")
        response = booking_api.get_booking_by_id(booking_id=absurd_id)
        
        logger.info("Step 2: Validating that the API returns 404 Not Found.")
        assert response.status_code == 404, f"Ghost data found! Expected 404, got {response.status_code}"
        logger.info("Success: API correctly reported that the resource does not exist.")

    def test_create_booking_with_missing_mandatory_field(self, booking_api):
        """
        Attempt to create a booking without the 'firstname' field.
        Expected: 500 Internal Server Error (or 400 Bad Request in a perfect API)
        """
        logger.info("Step 1: Preparing a payload with the mandatory 'firstname' field missing.")
        payload = generate_random_booking_payload()     
        del payload["firstname"]
        
        logger.info("Step 2: Sending the sabotaged payload to the API.")
        response = booking_api.create_booking(payload=payload)
        
        logger.info("Step 3: Validating that the API rejects the incomplete request.")
        # Restful-Booker crashes (500) when a field is missing, which is a known behavior.
        assert response.status_code == 500, f"Expected 500 Server Error, got {response.status_code}"
        logger.info("Success: API blocked the creation attempt due to missing data.")

    @pytest.mark.parametrize("test_data", load_boundary_payloads())
    def test_create_booking_with_boundary_values(self, booking_api, test_data):
        """
        Data-Driven Test: Inject malicious/boundary payloads from a JSON file.
        Verifies that the API properly rejects invalid or extreme data.
        """
        scenario_name = test_data["scenario"]
        payload = test_data["payload"]
        
        logger.info(f"Step 1: Starting boundary test execution for scenario: {scenario_name}")
        logger.info(f"Data injected: {payload}")
        
        response = booking_api.create_booking(payload=payload)
        
        logger.info("Step 2: Checking if the API defends itself against boundary values (400 or 500).")
        # Since we are intentionally using bad data, any rejection code (400 or 500) is technically a 'block'.
        assert response.status_code in [400, 500], \
            f"Security Breach! API accepted the payload for '{scenario_name}' and returned {response.status_code}!"
        
        logger.info(f"Result: API successfully blocked the '{scenario_name}' scenario.")