import os

class Config:
    """
    Configuration class to hold environment variables.
    """
    SELENIUM_HOST = os.getenv("SELENIUM_HOST", "localhost")
    SELENIUM_PORT = os.getenv("SELENIUM_PORT", "4444")
    SELENIUM_TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", 180))  # Default timeout for Selenium operations
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    EXECUTOR_TYPE = os.getenv("EXECUTOR_TYPE", "local") #Executor type can be "local" or "remote"

config = Config()