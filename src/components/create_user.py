from sqlalchemy.orm import Session
from sqlalchemy.orm import defaultload
from src.configuration.mysql_connection import DatabaseConnection
from src.models.models import User
from src.logger import logging
from src.exception import CustomException

class CreateUser:
    """Class to handle user creation with encrypted passwords."""

    def __init__(self):
        """Initialize database connection."""
        self.db_conn = DatabaseConnection()
        self.db: Session = self.db_conn.SessionLocal()

    def __create_user(self, name: str, email: str, password: str):
        """Create a new user with encrypted password."""
        try:
            
            # Insert new user into the database
            new_user = User(name=name, email=email, password=password)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            logging.info(f"User added with ID: {new_user.id}")
            return new_user
        
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error While Creating User : {e}")
            raise CustomException(e)

        finally:
            self.db.close()

    def initiate_create_user(self,name,email,password):
        try:
            self.__create_user(name=name,email=email,password=password)
        except Exception as e :
            raise CustomException(e)

        
