import pytest
from api.booking_api import BookingAPI
from api.auth_api import AuthAPI

@pytest.fixture(scope="session")
def booking_api():
    """Provides an instance of BookingAPI for all tests."""
    return BookingAPI()

@pytest.fixture(scope="session")
def auth_api():
    """Provides an instance of AuthAPI for all tests."""
    return AuthAPI()