from dotenv import load_dotenv
from dataclasses import dataclass
import os 

load_dotenv()

@dataclass
class EnvironmentVariables:
# Database Configuration
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")