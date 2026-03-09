import json
import allure
from core.logger import logger
from core.base_client import BaseClient

class BookingAPI(BaseClient):
    """
    Endpoints for the Restful-Booker Booking API.
    By putting (BaseClient) in the class definition, this class inherits 
    all the powerful methods (get, post, put, etc.) from our core engine.
    """

    def get_booking_ids(self):
        """Fetches all booking IDs. (GET /booking)"""
        logger.info("Fetching all booking IDs via GET /booking")
        
        response = self.get("/booking")

        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, "GET /booking")

        logger.info(f"Received response with status: {response.status_code}")
        return response

    def get_booking_by_id(self, booking_id: int):
        """Fetches a specific booking by its ID. (GET /booking/{id})"""
        logger.info(f"Fetching booking details for ID: {booking_id}")
        
        response = self.get(f"/booking/{booking_id}")

        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, f"GET /booking/{booking_id}")

        
        if response.status_code == 200:
            logger.info(f"Successfully retrieved booking ID: {booking_id}")
        else:
            logger.error(f"Failed to fetch booking ID: {booking_id}. Status: {response.status_code}")
        
        return response

    def create_booking(self, payload: dict):
        """Creates a new booking. (POST /booking)"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        logger.info(f"Creating a new booking with payload: {payload}")
        
        response = self.post("/booking", payload=payload, headers=headers)

        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, "POST /booking")

        if response.status_code in [200, 201]:
            # Try to safely extract the booking ID for the log
            booking_id = response.json().get('bookingid', 'Unknown')
            logger.info(f"Booking created successfully! Assigned ID: {booking_id}")
        else:
            logger.error(f"Failed to create booking. Status: {response.status_code}, Response: {response.text}")
            
        return response
    
    def update_booking(self, booking_id: int, payload: dict, token: str):
        """
        Updates a current booking entirely (PUT). 
        Requires an authentication token in the Cookie header.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }

        logger.info(f"Fully updating booking ID: {booking_id} with payload: {payload}")
        
        response = self.put(f"/booking/{booking_id}", payload=payload, headers=headers)
        
        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, f"PUT /booking/{booking_id}")

        if response.status_code == 200:
            logger.info(f"Successfully updated booking ID: {booking_id}")
        else:
            logger.error(f"Failed to update booking ID: {booking_id}. Status: {response.status_code}, Response: {response.text}")
            
        return response

    def partial_update_booking(self, booking_id: int, payload: dict, token: str):
        """
        Partially updates a booking (PATCH). 
        Example: Only updating the firstname. Requires Auth Token.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }
        
        logger.info(f"Partially updating booking ID: {booking_id} with payload: {payload}")
        
        response = self.patch(f"/booking/{booking_id}", payload=payload, headers=headers)

        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, f"PATCH /booking/{booking_id}")
        
        if response.status_code == 200:
            logger.info(f"Successfully patched booking ID: {booking_id}")
        else:
            logger.error(f"Failed to patch booking ID: {booking_id}. Status: {response.status_code}, Response: {response.text}")
            
        return response
    
    def delete_booking(self, booking_id: int, token: str):
        """
        Deletes a booking (DELETE). Requires Auth Token.
        """
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={token}"
        }

        logger.info(f"Attempting to delete booking ID: {booking_id}")
        
        response = self.delete(f"/booking/{booking_id}", headers=headers)
        
        # 📸 SNAPSHOT
        self.attach_api_response_to_allure(response, f"DELETE /booking/{booking_id}")
        
        if response.status_code == 201:
            logger.info(f"Successfully deleted booking ID: {booking_id}")
        else:
            logger.error(f"Failed to delete booking ID: {booking_id}. Status: {response.status_code}, Response: {response.text}")
            
        return response

    def attach_api_response_to_allure(self, response, endpoint_name):
        """Attaches the API's response to the Allure report in JSON/Text format."""
        try:
            formatted_data = json.dumps(response.json(), indent=4)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            formatted_data = response.text
            attachment_type = allure.attachment_type.TEXT

        allure.attach(
            body=formatted_data,
            name=f"📸 API Snapshot: {endpoint_name} | Status: {response.status_code}",
            attachment_type=attachment_type
        )