from faker import Faker
import random
from datetime import timedelta

fake = Faker(['nl_NL', 'en_US', 'de_DE', 'tr_TR'])

def generate_random_booking_payload() -> dict:
    """
    Generates a dynamic, randomized dictionary (payload) for booking creation.
    Every time this function is called, it produces entirely new data.
    """
    
    # We generate a random check-in date from this year
    checkin_date = fake.date_this_year()
    # Check-out should logically be AFTER check-in. So we add 1 to 14 random days to it.
    checkout_date = checkin_date + timedelta(days=random.randint(1, 14))
    
    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": random.randint(50, 5000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            # APIs usually expect dates in "YYYY-MM-DD" string format
            "checkin": checkin_date.strftime("%Y-%m-%d"),
            "checkout": checkout_date.strftime("%Y-%m-%d")
        },
        "additionalneeds": random.choice(["Breakfast", "Late Checkout", "Extra Towels", "None"])
    }
    
    return payload