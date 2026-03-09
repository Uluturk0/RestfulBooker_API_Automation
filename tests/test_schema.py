import pytest
from utils.data_generator import generate_random_booking_payload
from utils.assertions import assert_valid_schema
from core.logger import logger

class TestSchemaValidation:
    """
    Data Validation and Schema Consistency Tests.
    Ensures the API response strictly follows the defined JSON blueprints.
    """

    def test_booking_response_schema(self, booking_api):
        """
        Create a booking, fetch it, and rigorously validate the JSON schema 
        to ensure data types (int, string, boolean) are strictly respected.
        """
        
        # --- 1. Create a booking dynamically ---
        logger.info("Step 1: Generating dynamic payload and creating a new booking for schema testing.")
        payload = generate_random_booking_payload()
        create_response = booking_api.create_booking(payload=payload)
        
        assert create_response.status_code == 200, "Initial creation failed during schema test!"
        booking_id = create_response.json()["bookingid"]
        logger.info(f"Booking created with ID: {booking_id}")

        # --- 2. Fetch the booking (GET) ---
        logger.info(f"Step 2: Fetching the booking ID {booking_id} to get a clean JSON response.")
        get_response = booking_api.get_booking_by_id(booking_id=booking_id)
        
        assert get_response.status_code == 200, "Failed to fetch booking!"
        logger.info("Response received successfully from the server.")

        # --- 3. THE MAGIC: Schema Validation ---
        logger.info("Step 3: Rigorously validating the JSON schema against 'booking_schema.json'.")
        
        try:
            # We pass the JSON response and the name of our schema file to our detective.
            # If the API returns a string instead of an int for price, this will explode!
            assert_valid_schema(data=get_response.json(), schema_file="booking_schema.json")
            logger.info("Success: The JSON structure and data types are 100% compliant with the schema.")
        except Exception as e:
            logger.error(f"SCHEMA VALIDATION FAILED! The API contract has been broken. Details: {str(e)}")
            # We raise the exception again so Pytest can correctly mark the test as FAILED
            raise e