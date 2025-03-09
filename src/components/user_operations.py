from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.models import Transaction, Asset,User
from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection

class UserOperations:

    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db = self.conn.SessionLocal()
            logging.info("AssetTypeOperations initialized successfully")
        except Exception as e:
            logging.error(f"Database Connection Failed for AssetTypeOperations Component {CustomException(e)}")
            raise CustomException(e)
        
    
    def get_user_details(self):
        try:
            user_details = self.db.query(User.id,User.name,User.role).filter(User.role!="Admin").all()
            users_list = [{"id": user.id, "name": user.name, "role": user.role} for user in user_details]

            return users_list
        
        except SQLAlchemyError as e:
            logging.error(f"Database Error While Getting User Details: {CustomException(e)}")
            raise CustomException(e)
        
    def get_user_id(self, email):
        try:
            user = self.db.query(User).filter(User.email==email).first()
            return user.id if user else None
        
        except SQLAlchemyError as e:
            logging.error(f"Database Error While Getting User ID: {CustomException(e)}")
            raise CustomException(e)
        