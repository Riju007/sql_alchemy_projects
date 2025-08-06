"""Configuration for the project."""

# standard library imports
import os
from dotenv import load_dotenv

# 3rd party imports
from sqlalchemy import URL

ENV_FILE_PATH: str = ".dev.env"

load_dotenv(ENV_FILE_PATH)
# print(dotenv_values(ENV_FILE_PATH))
DATABASE_URL: str = URL.create(
    drivername=os.getenv("DRIVER_NAME"),
    username=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    database=os.getenv("DATABASE")
)
# print(DATABASE_URL)
