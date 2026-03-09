import pytest
from core.logger import logger
from utils.data_generator import generate_random_booking_payload

class TestPerformance:
    """
    Performance and SLA (Service Level Agreement) Tests.
    Verifies that the API responds within acceptable time limits.
    """
    # A strict limit for global performance standards
    MAX_RESPONSE_TIME_SECONDS = 2.0

    def test_create_booking_response_time(self, booking_api):
        """
        Measure the response time of the POST /booking endpoint.
        """
        logger.info("Step 1: Preparing a random payload for performance measurement.")
        payload = generate_random_booking_payload()
        
        logger.info("Step 2: Sending POST request and measuring elapsed time.")
        response = booking_api.create_booking(payload=payload)
        
        # Extracting the elapsed time from the response object
        response_time = response.elapsed.total_seconds()
        
        logger.info(f"Performance Result: POST /booking took {response_time:.4f} seconds.")
        
        logger.info("Step 3: Validating against SLA limits.")
        assert response.status_code == 200, "API failed to create booking!"
        
        assert response_time < self.MAX_RESPONSE_TIME_SECONDS, \
            f"API is too slow! Expected under {self.MAX_RESPONSE_TIME_SECONDS}s, but took {response_time}s"
        
        logger.info(f"Success: Response time ({response_time:.4f}s) is within the acceptable range.")

    def test_get_booking_response_time(self, booking_api):
        """
        Measure the response time of the GET /booking endpoint.
        """
        logger.info("Step 1: Requesting all booking IDs to measure GET performance.")
        response = booking_api.get_booking_ids()
        
        response_time = response.elapsed.total_seconds()
        
        logger.info(f"Performance Result: GET /booking took {response_time:.4f} seconds.")
        
        logger.info("Step 2: Validating against SLA limits.")
        assert response.status_code == 200, "API failed to fetch bookings!"
        
        assert response_time < self.MAX_RESPONSE_TIME_SECONDS, \
            f"GET API is too slow! Expected under {self.MAX_RESPONSE_TIME_SECONDS}s, but took {response_time}s"
        
        logger.info(f"Success: GET response time ({response_time:.4f}s) is within the acceptable range.")