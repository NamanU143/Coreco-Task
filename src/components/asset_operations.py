from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from src.models.models import Asset
from src.models.models import AssetTypes

class AssetOperations:

    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db = self.conn.SessionLocal()
            logging.info("AssetTypeOperations initialized successfully")
        except Exception as e:
            logging.error(f"Database Connection Failed for AssetTypeOperations Component {CustomException(e)}")
            raise CustomException(e)
        

    def add_asset(self, asset_type_id: int, asset_name: str, location: str, brand: str, purchase_year: int, 
                  is_active_asset: bool = True, current_owner: int = 1):
        try:
            new_asset = Asset(
                asset_type_id=asset_type_id,
                asset_name=asset_name,
                location=location,
                brand=brand,
                purchase_year=purchase_year,
                is_active_asset=is_active_asset,
                current_owner=current_owner
            )
            self.db.add(new_asset)
            self.db.commit()
            logging.info(f"Asset '{asset_name}' added successfully")
        except Exception as e:
            logging.info(f"Error adding asset rolling back")
            self.db.rollback()
            raise CustomException(f"Error occurred while adding asset: {CustomException(e)}")
        finally:
            self.db.close()


    def get_assets(self):
        try:
            assets = (self.db.query(Asset)
                      .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                      .filter(AssetTypes.is_active == True).order_by(Asset.asset_id).all())
            
            if len(assets) <= 0:
                logging.info("No asset types found in the database")
                return []
            logging.info(f"Found assets{assets}")
            return assets
        except Exception as e:
            raise CustomException(f"Error occurred while getting assets: {CustomException(e)}")
        finally:
            self.db.close()        

    def modify_asset(self, asset_id, asset_type_id, asset_name, location, brand, purchase_year):
        try:
            modify_asset = self.db.query(Asset).filter(Asset.asset_id == asset_id).one()
            modify_asset.asset_type_id = asset_type_id
            modify_asset.asset_name = asset_name
            modify_asset.location = location
            modify_asset.brand = brand
            modify_asset.purchase_year = purchase_year
            self.db.commit()
            logging.info(f"Asset with id {asset_id} modified successfully")
        except Exception as e:
            logging.info(f"Error in modifying asset rolling back")
            self.db.rollback()
            raise CustomException(f"Error occured while modifying asset {CustomException(e)}")  
        finally:
            self.db.close()


    def disable_asset(self, asset_id):

        try:
            disable_asset = self.db.query(Asset).filter(Asset.asset_id == asset_id).one()
            disable_asset.is_active_asset = False
            self.db.commit()
            logging.info(f"Asset with id {asset_id} disabled successfully")
        except Exception as e:
            logging.info(f"Error in enable asset rolling back")
            self.db.rollback()
            raise CustomException(f"Error occured while disabling asset {CustomException(e)}")
        finally:
            self.db.close()

    def enable_asset(self, asset_id):
        try:
            enable_asset = self.db.query(Asset).filter(Asset.asset_id == asset_id).one()
            enable_asset.is_active_asset = True
            self.db.commit()
            logging.info(f"Asset with id {asset_id} enabled successfully")
        except Exception as e:
            logging.info(f"Error in enable asset rolling back")
            self.db.rollback()
            raise CustomException(f"Error occured while enabling asset {CustomException(e)}")
        finally:
            self.db.close()

    def get_user_assets(self, user_id):
        try:
            assets = (
                self.db.query(Asset, AssetTypes.type_name)  # Selecting Asset and type_name
                .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                .filter(AssetTypes.is_active == True, Asset.current_owner == user_id, Asset.is_active_asset == True)
                .all()
            )

            if not assets:
                logging.info(f"No assets found for user {user_id}")
                return []

            # Formatting the response using chatgpt prompt look into the format in notes python
            asset_list = [
                {
                    "asset_id": asset.asset_id,
                    "asset_type_id": asset.asset_type_id,
                    "asset_name": asset.asset_name,
                    "type_name": type_name,
                    "location": asset.location,
                    "brand": asset.brand,
                    "purchase_year": asset.purchase_year,
                    "current_owner": asset.current_owner
                }
                for asset, type_name in assets  # this is like returning dictonary in list with list comprehension -- add to the materials.
            ]

            logging.info(f"Found {len(asset_list)} assets for user {user_id}")
            return asset_list

        except Exception as e:
            logging.error(f"Failed to find assets for user {user_id}: {str(e)}")
            raise CustomException(f"Error occurred while getting assets for user: {str(e)}")

        finally:
            self.db.close()

    def get_current_owner(self,asset_id):
        try:
            current_owner = self.db.query(Asset.current_owner).filter(Asset.asset_id == asset_id).first()

            if current_owner:
                return current_owner[0]
            else:
                return None
        except Exception as e:
            logging.info(f"Failed to get current owner for asset id {asset_id}")
            raise CustomException(f"Error getting current owner for asset {CustomException(e)}")
        
    def get_asset_details(self, asset_id):
        try:
            asset_details = (
                self.db.query(Asset, AssetTypes.type_name)
                .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                .filter(Asset.asset_id == asset_id)
                .first()
            )


            if asset_details:
                logging.info(f"asset details - > {asset_details.asset_id}")
                asset, type_name = asset_details  # Unpacking tuple

                return {
                    "asset_id": asset.asset_id,
                    "asset_type_id": asset_details.asset_type_id,
                    "type_name": type_name,
                    "asset_name": asset.asset_name,
                    "location": asset.location,
                    "brand": asset.brand,
                    "purchase_year": asset.purchase_year,
                    "current_owner": asset.current_owner
                }
        except Exception as e:
            logging.info(f"Failed to get asset details for asset id ")
            raise CustomException(f"Error getting asset details for asset {CustomException(e)}")
        finally:
            self.db.close()

    


