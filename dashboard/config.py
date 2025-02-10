from os import getenv
from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    """
    A class to configure global settings for the application.

    This class retrieves the configuration values from environment variables 
    and provides default values in case the environment variables are not set.

    Attributes:
        BACKEND_URL (str): The URL of the backend API. Defaults to "http://localhost:8000/api/v1".
        CACHE_VALID_DURATION (int): Duration (in seconds) for caching. Defaults to 600 seconds (10 minutes).
    """
    
    BACKEND_URL: str = getenv("BACKEND_URL", "http://localhost:8000/api/v1")
    CACHE_VALID_DURATION: int = int(getenv("CACHE_VALID_DURATION", 600))

global_settings = GlobalConfig()