from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from src.constants.db_constants import EnvironmentVariables as ev
from dotenv import load_dotenv
from src.exception import CustomException
from src.logger import logging

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Database connection using sqlalchemy."""

    def __init__(self):
        try:
            # MySQL Connection url for sqlalchemy
            # DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
            DATABASE_URL = f"mysql+mysqlconnector://{ev.MYSQL_USER}:{ev.MYSQL_PASSWORD}@{ev.MYSQL_HOST}/{ev.MYSQL_DATABASE}"
            
            self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
            self.Base = declarative_base()
            logging.info("Database Connection Sucessful !!!")
        except Exception as e:
            logging.info(f"Error initializing connection to MySql Database {CustomException(e)}")
            raise CustomException(e)


    def get_db(self):
        """Provides a database session. 
            Use by calling SessionLocal()
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()



##########################
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# print(os.getenv('MYSQL_USER'))
# print(os.getenv('MYSQL_PASSWORD'))
# print(os.getenv('MYSQL_HOST'))
# print(os.getenv('MYSQL_DATABASE'))

# # MySQL Connection URL for SQLAlchemy
# DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"


# # Create Engine
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# # Create Session
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# # Base class for ORM models
# Base = declarative_base()

# # Dependency function to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
