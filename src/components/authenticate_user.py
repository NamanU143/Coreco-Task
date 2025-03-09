from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.models import User


class AuthenticateUser:
    """Class to Authenticate User"""
    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db:Session = self.conn.SessionLocal()
            logging.info("MySql Database Connection Sucessfull for User Exists Component !!!")
        except Exception as e:
            logging.error(f"Database Connection Failed for User Exists Component {CustomException(e)}")

    def verify_password(self,password,email):
        try:
            self.user = self.db.query(User).filter(User.email == email).first()
            if self.user.password == password:
                return True
            else :
                return False
                        
        except SQLAlchemyError as e :
            logging.error(f"Database Error While Authenticating User Password: {CustomException(e)}")
            raise CustomException(e)
        
        finally:
            self.db.close()