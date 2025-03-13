from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from src.models.models import Asset
from src.models.models import AssetTypes,User

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
            assets = (self.db.query(
                        Asset.asset_id,
                        Asset.asset_name,
                        Asset.location,
                        Asset.brand,
                        Asset.purchase_year,
                        Asset.is_active_asset,
                        AssetTypes.type_name.label("asset_type"),
                        User.name.label("current_owner_name"),
                        Asset.current_owner
                    )
                    .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                    .join(User, Asset.current_owner == User.id)
                    .filter(AssetTypes.is_active == True, Asset.is_active_asset == True)
                    .order_by(Asset.asset_id)
                    .all())

            if not assets:
                logging.info("No assets found in the database")
                return []

            # this is how we convert the sqlalchemy returned object to dictonary instead of looping for every metric
            assets_list = [dict(asset._asdict()) for asset in assets]

            logging.info(f"Found assets: {assets_list}")
            return assets_list

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
                self.db.query(Asset, AssetTypes.type_name, User.name)
                .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                .join(User, Asset.current_owner == User.id)
                .filter(Asset.asset_id == asset_id)
                .first()
            )

            if asset_details:
                asset, type_name, current_owner_name = asset_details  # Unpacking tuple

                logging.info(f"Asset details -> asset_id: {asset.asset_id}")
                logging.info(f"Asset details -> current owner name: {current_owner_name}")


                return {
                    "asset_id": asset.asset_id,
                    "asset_type_id": asset.asset_type_id,  # Fixed attribute access
                    "type_name": type_name,
                    "asset_name": asset.asset_name,
                    "location": asset.location,
                    "brand": asset.brand,
                    "purchase_year": asset.purchase_year,
                    "current_owner": current_owner_name,  # Correctly fetching name
                    "current_owner_id":asset.current_owner
                }

        except Exception as e:
            logging.error(f"Failed to get asset details for asset id {asset_id}: {str(e)}")
            raise CustomException(f"Error getting asset details for asset {asset_id}: {str(e)}")

        finally:
            self.db.close()


    def get_user_assets(self, user_id):
        try:
            user_assets = (
                self.db.query(Asset, AssetTypes.type_name)
                .join(AssetTypes, Asset.asset_type_id == AssetTypes.asset_type_id)
                .filter(Asset.current_owner == user_id)
                .all()
            )
            if not user_assets:
                logging.info("No assets found for the user")
                return []
            user_assets = [dict(asset._asdict()) for asset in user_assets]
            logging.info(f"Found assets for user id {user_id}: {user_assets}")
            return user_assets
        
        except Exception as e:
            logging.error(f"Failed to get user assets for user id {user_id}: {str(e)}")
            raise CustomException(f"Error getting user assets for user {user_id}: {str(e)}")
        finally:
            self.db.close()
        