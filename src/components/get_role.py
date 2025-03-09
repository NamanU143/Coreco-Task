from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.models import User


class UserRole :
    """Class to get user role ."""
    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db: Session = self.conn.SessionLocal()
            logging.info("MySql Database Connection Sucessfull for User Role Component!!!")
        except Exception as e:
            logging.error(f"Database Connection Failed for User Role Component {CustomException(e)}")
            raise CustomException(e)
        
    def get_user_role(self, email: str) -> str:
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user.role if user else None
        
        except SQLAlchemyError as e:
            logging.error(f"Database Error While Getting User Role: {CustomException(e)}")
            raise CustomException(e)
