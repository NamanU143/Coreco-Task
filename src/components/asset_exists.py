from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection  
from src.models.models import Asset

class AssetExists:
    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db:Session = self.conn.SessionLocal()
            logging.info("MySql Database Connection Sucessfull for Asset Type Exists Component !!!")
        except Exception as e:
            logging.error(f"Database Connection Failed for Asset Type Exists Component {CustomException(e)}")

    def asset_exists(self, asset_id:int) -> bool:

        try:
            # checking if is active true and typename
            exists = self.db.query(Asset).filter(Asset.asset_id == asset_id ).first() #and Asset.is_active_asset==True
            return exists is not None  

        except SQLAlchemyError as e:
            logging.error(f"Database Error While Checking Asset Type Exists: {CustomException(e)}")
            raise CustomException(e)
        
        finally:
            self.db.close()
