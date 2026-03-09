from core.logger import logger
from utils.data_generator import generate_random_booking_payload

class TestBookingE2E:
    """
    End-to-End Test Suite for Booking Operations.
    This class verifies the complete lifecycle of a booking (CRUD).
    Powered by dynamic data generation (Faker).
    """

    def test_full_booking_lifecycle(self, booking_api, auth_api):
        """
        Scenario: Create -> Read -> Authenticate -> Update -> Delete -> Verify Deletion
        """
        
        # --- 1. DYNAMIC CREATE (POST) ---
        logger.info("Step 1: Generating dynamic payload and creating a new booking.")
        payload = generate_random_booking_payload()
        expected_firstname = payload["firstname"]
        expected_totalprice = payload["totalprice"]
        
        create_response = booking_api.create_booking(payload=payload)
        assert create_response.status_code == 200, f"Failed to create booking! Status: {create_response.status_code}"
        
        booking_id = create_response.json()["bookingid"]
        logger.info(f"Booking successfully created with ID: {booking_id}")
        
        # --- 2. DYNAMIC READ (GET) ---
        logger.info(f"Step 2: Fetching the newly created booking ID: {booking_id} to verify data integrity.")
        get_response = booking_api.get_booking_by_id(booking_id=booking_id)
        assert get_response.status_code == 200, "Failed to fetch the created booking!"

        actual_firstname = get_response.json()["firstname"]
        assert actual_firstname == expected_firstname, f"Data Mismatch! Expected {expected_firstname}, but got {actual_firstname}"
        logger.info(f"Verification successful: Firstname '{actual_firstname}' matches the payload.")
        
        # --- 3. AUTHENTICATE (Get VIP Ticket) ---
        logger.info("Step 3: Requesting authentication token for secure operations (Update/Delete).")
        token_response = auth_api.create_token()
        assert token_response.status_code == 200, "Failed to generate authentication token!"
        token = token_response.json()["token"]
        logger.info("Authentication successful. Token received.")
        
        # --- 4. DYNAMIC UPDATE (PUT) ---
        logger.info(f"Step 4: Performing a full update (PUT) on booking ID: {booking_id}")
        updated_payload = payload.copy()
        updated_payload["firstname"] = "Updated" + expected_firstname
        updated_payload["totalprice"] = int(round(expected_totalprice * 1.10))
        
        update_response = booking_api.update_booking(booking_id=booking_id, payload=updated_payload, token=token)
        assert update_response.status_code == 200, "Failed to update booking!"

        updated_firstname = update_response.json()["firstname"]
        assert updated_firstname == updated_payload["firstname"], f"Update verification failed! Got {updated_firstname}"
        logger.info(f"Update successful: Name changed to '{updated_firstname}' and price increased.")
        
        # --- 5. DELETE ---
        logger.info(f"Step 5: Deleting booking ID: {booking_id}")
        delete_response = booking_api.delete_booking(booking_id=booking_id, token=token)
        # API returns 201 Created for successful deletion
        assert delete_response.status_code == 201, f"Delete operation failed! Status: {delete_response.status_code}"
        logger.info(f"Delete command accepted by server for ID: {booking_id}")
        
        # --- 6. VERIFY DELETION (GET again, expect 404) ---
        logger.info(f"Step 6: Final verification. Attempting to fetch deleted ID: {booking_id} (Expecting 404).")
        verify_delete_response = booking_api.get_booking_by_id(booking_id=booking_id)
        assert verify_delete_response.status_code == 404, "Security/Logic Gap: Booking was not actually deleted!"
        logger.info("Final verification passed: Booking is no longer accessible. E2E Cycle Complete.")