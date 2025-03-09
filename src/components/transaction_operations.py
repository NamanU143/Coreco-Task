from src.models.models import Transaction, Asset,User
from src.logger import logging
from src.exception import CustomException
from src.configuration.mysql_connection import DatabaseConnection
from sqlalchemy.exc import SQLAlchemyError

class Transactions:

    def __init__(self):
        try:
            self.conn = DatabaseConnection()
            self.db = self.conn.SessionLocal()
            logging.info("AssetTypeOperations initialized successfully")
        except Exception as e:
            logging.error(f"Database Connection Failed for AssetTypeOperations Component {CustomException(e)}")
            raise CustomException(e)
        
    def transfer_owner(self,asset_id,from_user_id,to_user_id):
        try:
            asset = self.db.query(Asset).filter(Asset.asset_id == asset_id).first()

            if asset.current_owner == from_user_id:
                asset.current_owner = to_user_id
            
            else :
                message = f"from user_id is not current owner of asset {asset_id}"
                return message
            
            transaction = Transaction(
                asset_id=asset_id, 
                from_user_id=from_user_id, 
                to_user_id=to_user_id
                )
                
            self.db.add(transaction)
            self.db.commit()
            logging.info(f"Transferred asset id {asset_id} from user_id {from_user_id} to user_id {to_user_id} successfully")
                
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error during transaction {CustomException(e)}")
            raise CustomException(e)
        finally:
            self.db.close()
        
    def get_user_transactions(self, user_id):

        try:
            transactions = (
                self.db.query(Transaction, Asset, User)
                .join(Asset, Transaction.asset_id == Asset.asset_id)
                .join(User, Transaction.to_user_id == User.id)
                .filter(
                    (Transaction.from_user_id == user_id) | (Transaction.to_user_id == user_id)
                )
                .all()
            )

            if not transactions:
                return []

            transaction_list = []
            for transaction, asset, user in transactions:
                transaction_list.append({
                    "transaction_id": transaction.transaction_id,
                    "asset_id": asset.asset_id,
                    "asset_name": asset.asset_name,
                    "from_user": transaction.from_user_id,  
                    "to_user": user.id,  
                    "transfer_date": transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S")
                })

            return transaction_list

        except SQLAlchemyError as e:
            logging.error(f"Error fetching transactions for user {user_id}: {CustomException(e)}")
            raise CustomException(e)
        finally:
            self.db.close()