# This file defines all configuration values the app needs
# (DB connection info, app name, etc)

# pydantic_settings : Automatically reads environment variables and their types
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    #MongoDB settings
    MONGO_URI : str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "e_commerce_customer_support"

    #Gives the app a name
    APP_NAME : str = "E-Commerce Customer Support App API"

    #Informs pydantic_settings to load values from .env file for all the data
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

# Shared Settings Object that all other files can import 
settings = Settings()
