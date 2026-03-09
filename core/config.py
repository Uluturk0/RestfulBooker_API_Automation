import os
from dotenv import load_dotenv

# This function automatically finds the .env file in your root folder and loads its variables into memory.
load_dotenv()

class Config:
    """
    Configuration class to securely fetch environment variables.
    Instead of typing os.getenv() everywhere in our framework, 
    we will just call Config.BASE_URL. This prevents typos and keeps code clean.
    """
    BASE_URL = os.getenv("BASE_URL")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # We can also set default timeout values for our API requests globally here
    DEFAULT_TIMEOUT = 10