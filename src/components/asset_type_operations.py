from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from src.models.models import AssetTypes

class AssetTypeOperations:

    def __init__(self):
        self.conn = DatabaseConnection()
        self.db = self.conn.SessionLocal()
        logging.info("AssetTypeOperations initialized successfully")
    
    def get_asset_types(self):
        try:
            asset_types = self.db.query(AssetTypes).all()
            if len(asset_types) <= 0:
                logging.info("No asset types found in the database")
                return []
            return asset_types
        except Exception as e:
            raise CustomException(f"Error occurred while getting asset types: {CustomException(e)}")
        finally:
            self.db.close()

    def create_asset_type(self, type_name):
        try:
            new_asset_type = AssetTypes(type_name=type_name)
            self.db.add(new_asset_type)
            self.db.commit()
            new_asset_type.is_active=True
            logging.info(f"Asset type '{type_name}' created successfully")
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error occurred while creating asset type: {CustomException(e)}")
        finally:
            self.db.close()
    
    def update_asset_type(self,type_name,new_type_name):
        try:
            update_asset = self.db.query(AssetTypes).filter(AssetTypes.type_name==type_name).one()
            if update_asset:
                update_asset.type_name = new_type_name
                self.db.commit()
                logging.info(f"Asset type '{update_asset.type_name}' to {type_name} Updated successfully")
        except Exception as e :
            self.db.rollback()
            logging.error(f"Error occured while updating asset type {CustomException(e)}")
            raise CustomException(e)
        finally:
            self.db.close()


    def disable_asset_type(self,type_name):
        try:
            asset_type = self.db.query(AssetTypes).filter(AssetTypes.type_name==type_name).one()
            if asset_type :
                asset_type.is_active = False
                self.db.commit()
                logging.info(f"Asset type {type_name} disabled !!! ")
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error occured while disabling asset type {type_name}:  {CustomException(e)}")
        finally:
            self.db.close()

    def enable_asset_type(self,type_name):
        try:
            asset_type = self.db.query(AssetTypes).filter(AssetTypes.type_name==type_name).one()
            if asset_type :
                asset_type.is_active = True
                self.db.commit()
                logging.info(f"Asset type {type_name} enabled !!! ")
        except Exception as e:
            self.db.rollback()
            raise CustomException(f"Error occured while enabling asset type {type_name}:  {CustomException(e)}")
        finally:
            self.db.close()

    def get_asset_type_id(self, type_name):
        try:
            asset_type = self.db.query(AssetTypes).filter(AssetTypes.type_name==type_name).first()
            if asset_type :
                return asset_type.asset_type_id
            else:
                return None
        except Exception as e:
            raise CustomException(f"Error occurred while getting asset type id: {CustomException(e)}")
        finally:
            self.db.close()