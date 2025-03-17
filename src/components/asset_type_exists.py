from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection  
from src.models.models import AssetTypes

class AssetTypeExists:
    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db: Session = self.conn.SessionLocal()
            logging.info("MySQL Database Connection Successful for Asset Type Exists Component!")
        except Exception as e:
            logging.error(f"Database Connection Failed for Asset Type Exists Component: {CustomException(e)}")
            raise CustomException(e)

    def asset_type_exists(self, type_name: str) -> bool:
        try:
            exists = self.db.query(AssetTypes).filter(
                AssetTypes.type_name == type_name,
            ).first()

            return exists is not None  

        except SQLAlchemyError as e:
            logging.error(f"Database Error While Checking Asset Type Exists: {CustomException(e)}")
            raise CustomException(e)
        
        finally:
            self.db.close()  # Ensure session is closed after operation
