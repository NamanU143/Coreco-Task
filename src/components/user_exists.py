from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection  
from src.models.models import User
from typing import Optional

class UserExists:
    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db: Session = self.conn.SessionLocal()
            logging.info("MySQL Database Connection Successful for User Exists Component!")
        except Exception as e:
            logging.error(f"Database Connection Failed for User Exists Component: {CustomException(e)}")
            raise CustomException(e)

    def user_exists(self, email: Optional[str] = None, user_id: Optional[int] = None) -> bool:
        """
        Checks if a user with the given email or user_id exists in the database.
        """
        try:
            logging.info(f"Email in user exists {email}")
            logging.info(f"User Id in user exists {user_id}")
            if email:
                exists = self.db.query(User).filter(User.email == email).first()
            elif user_id:
                exists = self.db.query(User).filter(User.id == user_id).first()  # Fix: Use correct column name
            else:
                logging.warning("No email or user_id provided for user existence check.")
                return False  # Return False explicitly if no parameters are given

            logging.info(f"===> user exists ---> {exists}")
            return False if exists is None else True

        except SQLAlchemyError as e:
            logging.error(f"Database Error While Checking User Exists: {str(e)}")
            raise CustomException(f"Database error: {str(e)}")
