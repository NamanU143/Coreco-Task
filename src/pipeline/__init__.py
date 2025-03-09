from src.logger import logging
from src.exception import CustomException
from datetime import date
from src.components.user_exists import UserExists
from src.components.encrypt_password import EncryptPassword
from src.components.create_user import CreateUser
from src.components.authenticate_user import AuthenticateUser
from src.components.get_role import UserRole
from src.components.asset_type_exists import AssetTypeExists
from src.components.asset_type_operations import AssetTypeOperations
from src.components.asset_operations import AssetOperations
from src.components.asset_exists import AssetExists
from src.components.user_operations import UserOperations
from typing import Optional
from src.components.transaction_operations import Transactions



class Pipeline:
    def __init__(self):
        try :
            logging.info("-------------------------------------------Pipeline initialized successfully------------------------------------")
        except Exception as e :
            logging.info(f"Error Initializing Pipeline - (pipeline init) {CustomException(e)} ")
            raise CustomException(e)

    def __call_get_user_id(self,email):
        try:
            useroperations = UserOperations()
            user_id = useroperations.get_user_id(email=email)
            return user_id
        except Exception as e:
            logging.info(f"Error Calling User Operations Component (get user id) {CustomException(e)}")
            raise CustomException(e)
    def __call_user_exists(self,email:Optional[str]=None,user_id:Optional[int]=None):
        try:
            userexists = UserExists()
            return userexists.user_exists(email=email,user_id=user_id)
            
        except Exception as e :
            logging.info(f"Error Calling User Exists Component - (user exists) {CustomException(e)} ")
            raise CustomException(e)

    def __call_encrypt_password(self, password):
        try:
            encryptpassword = EncryptPassword(password=password)
            encrypted_password = encryptpassword.initiate_encryption()
            return encrypted_password
        except Exception as e:
            logging.info(f"Error Calling Encrypt Password Component (encrypt password) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_create_user(self,name,email,password):
        try:
            newuser = CreateUser()
            newuser.initiate_create_user(name=name,email=email,password=password)
        except Exception as e:
            logging.info(f"Error Calling Create User Component (create user) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_authenticate_user(self,email,password):
        try:
            authenticateuser = AuthenticateUser()
            return authenticateuser.verify_password(email=email,password=password)
        except Exception as e:
            logging.info(f"Error Calling Create User Component (authenticate user) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_get_role(self,email):
        try:
            userrole = UserRole()
            role = userrole.get_user_role(email=email)
            return role
        except Exception as e:
            logging.info(f"Error Calling Get Role Component (get role) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_asset_type_exists(self,type_name):
        try:
            assettypeexists = AssetTypeExists()
            return assettypeexists.asset_type_exists(type_name=type_name)
        except Exception as e:
            logging.info(f"Error Calling AssetTypeExists Component (asset type exists) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_add_asset_type(self,type_name):
        try:
            logging.info("<<< Calling AssetTypeExists Component")
            addasset = AssetTypeOperations()
            addasset.create_asset_type(type_name=type_name)
            logging.info(">>> Completed Adding Asset Type")
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (add asset type) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_update_asset_type(self,type_name,new_type_name):
        try:
            logging.info("<<< Calling AssetTypeOperations Component")
            updateasset = AssetTypeOperations()
            updateasset.update_asset_type(type_name=type_name, new_type_name=new_type_name)
            logging.info(">>> Completed Updating Asset Type")
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (update asset type) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_disable_asset_type(self,type_name):
        try:
            logging.info("<<< Calling AssetTypeOperations Component")
            disableasset = AssetTypeOperations()
            disableasset.disable_asset_type(type_name=type_name)
            logging.info(">>> Completed Disabling Asset Type")
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (disable asset type) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_enable_asset_type(self,type_name):
        try:
            logging.info("<<< Calling AssetTypeOperations Component")
            enableasset = AssetTypeOperations()
            enableasset.enable_asset_type(type_name=type_name)
            logging.info(">>> Completed Enabling Asset Type")
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (enable asset type) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_get_asset_types(self):
        try:
            logging.info("<<< Calling AssetTypeOperations Component")
            getassettypes = AssetTypeOperations()
            asset_types = getassettypes.get_asset_types()
            logging.info(">>> Completed Getting Asset Types")
            return asset_types
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (get asset types) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_asset_exists(self,asset_id):
        try:
            logging.info("<<< Calling Asset Exists Component")
            assetexists = AssetExists()
            return assetexists.asset_exists(asset_id=asset_id)
        except Exception as e:
            logging.info(f"Error Calling Asset Exists Component (asset exists) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_get_asset(self):
        try:
            logging.info("<<< Calling AssetOperations Component")
            getassets = AssetOperations()
            assets = getassets.get_assets()
            logging.info(">>> Completed Getting Assets")
            return assets
        except Exception as e:
            logging.info(f"Error calling AssetOperations Component (get asset) {CustomException(e)}")       
            raise CustomException(e)
    
    def __call_get_asset_details(self,asset_id):
        try:
            logging.info("<<< Calling AssetOperations Component")
            getassetdetails = AssetOperations()
            asset_details = getassetdetails.get_asset_details(asset_id=asset_id)
            logging.info(">>> Completed Getting Asset Details")
            return asset_details
        except Exception as e:
            logging.info(f"Error Calling AssetOperations Component (get asset details) {CustomException(e)}")
            raise CustomException(e)
    def __call_get_asset_type_id(self,type_name):
        try:
            logging.info("<<< Calling AssetTypeOperations Component")
            getassettypeid = AssetTypeOperations()
            asset_type_id = getassettypeid.get_asset_type_id(type_name=type_name)
            logging.info(">>> Completed Getting Asset Type ID")
            return asset_type_id
        except Exception as e:
            logging.info(f"Error Calling AssetTypeOperations Component (get asset type id) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_add_asset(self,asset_type_id,asset_name,location,brand,purchase_year):
        try:
            logging.info("Calling AssetOperations Component for adding asset")
            addassets = AssetOperations()
            addassets.add_asset(asset_type_id=asset_type_id,asset_name=asset_name,location=location,brand=brand,
                                purchase_year=purchase_year) # is_active_asset,current_owner
            logging.info(">>> Completed Adding Asset")
        except Exception as e:
            logging.info(f"Error Calling AssetOperations Component (add asset) {CustomException(e)}")
            raise CustomException(e)
        
    def __call_modify_asset(self, asset_id, asset_type_id, asset_name, location, brand, purchase_year):
        try:
            logging.info("<<< Calling AssetOperations Component for modifying asset")
            modifyassets = AssetOperations()
            modifyassets.modify_asset(asset_id=asset_id, asset_type_id=asset_type_id, asset_name=asset_name, 
                                      location=location, brand=brand, purchase_year=purchase_year)
        except Exception as e :
            logging.info(f"Error Calling AssetOperations Component (modify asset)")
            raise CustomException(e)
        
    def __call_disable_asset(self,asset_id):
        try:
            logging.info("<<< Calling AssetOperations Component for disabling asset")
            disableasset = AssetOperations()
            disableasset.disable_asset(asset_id=asset_id)  
        except Exception as e:
            logging.error("Error Calling AssetOperations Component (disable asset)")
            raise CustomException(e)     

    def __call_enable_asset(self,asset_id):
        try:
            logging.info("<<< Calling AssetOperations Component for enabling asset")
            enableasset = AssetOperations()
            enableasset.enable_asset(asset_id=asset_id)
        except Exception as e:
            logging.error("Error Calling AssetOperations Component (enable asset)")
            raise CustomException(e) 

    def __call_get_user_assets(self,user_id):
        try:
            logging.info("<<< Calling AssetOperations for getting user assets")
            getassets = AssetOperations()
            user_assets = getassets.get_user_assets(user_id=user_id)
            return user_assets
        except Exception as e:
            logging.error(f"Error in Calling AssetOperations Component (get user assets) {CustomException(e)}")
            raise CustomException(e)

    def __call_transfer_owner(self,asset_id,from_user_id,to_user_id):
        try:
            logging.info("<<< Calling AssetOperations for getting transactions")
            gettransactions = Transactions()
            message:Optional[str] = gettransactions.transfer_owner(asset_id=asset_id, from_user_id=from_user_id, to_user_id=to_user_id)
            return message
        except Exception as e:
            logging.error(f"Error in Calling AssetOperations Component (get transactions) {CustomException(e)}")
            raise CustomException(e)

    def __call_get_user_details(self):
        try:
            logging.info("<<< Calling UserOperations for getting user details")
            getuserdetails = UserOperations()
            user_details = getuserdetails.get_user_details()
            return user_details
        except Exception as e:
            logging.error(f"Error in Calling UserOperations Component (get user details) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_get_user_transactions(self,user_id):
        try:
            logging.info("<<< Calling Transactions Component for getting user transactions")
            gettransactions = Transactions()
            user_transactions = gettransactions.get_user_transactions(user_id=user_id)
            return user_transactions
        except Exception as e:
            logging.error(f"Error in Calling Transactions Component (get user transactions) {CustomException(e)}")
            raise CustomException(e)
    
    def __call_get_current_owner(self,asset_id):
        try:
            logging.info("<<< Calling Transaction Component for getting current owner")
            getcurrentowner = AssetOperations()
            currentowner = getcurrentowner.get_current_owner(asset_id=asset_id)
            return currentowner
        except Exception as e:
            logging.error(f"Error in Calling Transaction Component (get current owner) {CustomException(e)}")
            raise CustomException(e)       

###########################################################################################################################################
###########################################################################################################################################

# PIPELINES

    def initiate_registration_pipeline(self,name,email,password):
        try:
            logging.info("<<< Initiating Pipeline")
            
            logging.info("<<< Checking If User Exists In Database")
            userexist = self.__call_user_exists(email=email)

            if userexist :
                return {
                    "userExists":True,
                    "message":"User Already Exists Please Login"
                }
            
            logging.info("<<< Calling Encrypt Password Component")
            encryptedpassword = self.__call_encrypt_password(password=password)
            logging.info(">>> Completed Password Encryption")

            logging.info("<<< Calling Create User Component")
            self.__call_create_user(name=name,email=email,password=password)
            logging.info(">>> Completed Creating User")


            logging.info("<<< Calling Get Role Component")
            role = self.__call_get_role(email=email)
            logging.info(f"User Role for email {email} is {role}")
            logging.info(f">>> Completed Get Role Component")

            logging.info("Completed Registration Pipeline !!!")
            return {

                "userExists":False,
                "role": role,
                "message":"User Created Successfully. Please Login"
            }
    
        except Exception as e :
            logging.info(f"!!! Error Registration Pipeline !!! - {CustomException(e)} ")
            raise CustomException(e)
        
    def initiate_login_pipeline(self,email,password):
        try:
            logging.info("<<< Initiating Pipeline")
            
            logging.info("<<< Checking If User Exists In Database")
            userexist = self.__call_user_exists(email=email)
            logging.info("<<< Completed User Exists Component")

            if not userexist :
                logging.info(f"User dont exist for email {email}")
                return {
                    "userExists":False,
                    "message":"Email not found. Please check your email address or register for a new account."
                }
            
            logging.info(f"Authenticating the password for user")
            password_verification = self.__call_authenticate_user(email=email,password=password)

            logging.info("<<< Calling Get Role Component")
            role = self.__call_get_role(email=email)
            logging.info(f"User Role for email {email} is {role}")
            logging.info(f">>> Completed Get Role Component")

            logging.info(f"Get User Id for email {email}")
            user_id = self.__call_get_user_id(email=email)
            logging.info("<<< Completed Get User Id Component")
            
            logging.info("!!! Completed Login Pipeline !!!")

            if password_verification :
                return {
                    "user_id": user_id,
                    "role":role,
                    "passwordVerified":True,
                    "message":f"password verified for email : {email}"
                }
            else :
                return {
                    "passwordVerified":False,
                    "message":f"password not verified for email : {email} ,check your password"
                }
            
        except Exception as e :
            logging.error(f"!!! Error in Login Pipeline !!! - {CustomException(e)}")
            raise CustomException(e)
        
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Asset Types 

    # add asset type
    def initiate_add_asset_type_pipeline(self,asset_type_name):
        try:
            logging.info("<<< Initiating add asset type pipeline")

            logging.info("<<< Calling Asset Type Exists Component") 
            assetexists = self.__call_asset_type_exists(type_name=asset_type_name)
            logging.info("<<< Completed Asset Type Exists In Database") 

            if assetexists :
                return {
                    "assettypeexists" : True,
                    "message":"Asset already exists in the database"
                }
            
            logging.info("<<< Adding New Asset Type In the Database")
            self.__call_add_asset_type(type_name=asset_type_name)
            logging.info("<<< Calling Create Asset Type Component")

            logging.info("!!! Completed add asset type pipeline")
            return {
                "assettypeexists":False,
                "message":"Asset added successfully"
            }
        
        except Exception as e :
            logging.error(f"!!! Error in add asset type pipeline !!! - {CustomException(e)}")
            raise CustomException(e)

    # modify asset type
    def initiate_modify_asset_type_pipeline(self,type_name,new_type_name):

        try:
            logging.info(f"<<< Initiating modify for asset type pipeline")
            
            logging.info("<<< Calling Asset Type Exists Component")
            assettypeexists = self.__call_asset_type_exists(type_name=type_name)
            logging.info("<<< Completed Asset Type Exists Component")

            logging.info("<<< Checking if new asset type already exists in database")
            newassettypeexists = self.__call_asset_type_exists(type_name=new_type_name)
            logging.info("<<< Completed Checking If New Asset Type Exists Component")

            if newassettypeexists :
                return {
                    "assettypeexists":assettypeexists,
                    "newassettypeexists":newassettypeexists,
                    "message":"New asset type already exists in the database"
                }


            if not assettypeexists :
                return {
                    "assettypeexists" : assettypeexists,
                    "message":"Asset does not exist in the database"
                }
            
            logging.info("<<< Initiated Modifying Asset Type In the Database")
            self.__call_update_asset_type(type_name=type_name,new_type_name=new_type_name)


            logging.info(">>> Completed Modify Asset Type Component")

            logging.info("!!! Completed modify asset type pipeline")
            return {
                "assettypeexists":True,
                "message":"Asset type modified successfully"
            }
        
        except Exception as e :
            logging.error(f"!!! Error in modify asset type pipeline !!! - {CustomException(e)}")
            raise CustomException(e)

    # disable asset type
    def initiate_soft_disable_asset_type_pipeline(self,type_name):
        try:
            logging.info(f"<<< Initiating soft delete for asset type pipeline")
            
            logging.info("<<< Initiated Asset Type Exists Component")
            assetexists = self.__call_asset_type_exists(type_name=type_name)
            logging.info("<<< Completed Asset Type Exists Component")
            
            if not assetexists :
                logging.info("<<< Asset type not found in database")
                return {
                    "assettypeexists" : False,
                    "assetTypeDisabled":False,
                    "type_name":type_name,
                    "message":"Asset does not exist in the database"
                }
            
            logging.info("Initiated Disable Asset Type Operation")
            self.__call_disable_asset_type(type_name=type_name)
            logging.info("Completed Disable Asset Type Operation")

            logging.info("!!! Completed soft delete asset type pipeline")
            return {
                "assettypeexists":True,
                "assetTypeDisabled":True,
                "type_name":type_name,
                "message":"Asset type soft deleted successfully"
            }
        
        except Exception as e :
            logging.error(f"!!! Error in disable asset type pipeline !!! - {CustomException(e)}")
            raise CustomException(e)

    # enable asset type
    def initiate_enable_asset_types_admin_pipeline(self,type_name):

        try:
            logging.info(f"<<< Initiating enable asset types pipeline")

            logging.info("<<< Initiated Asset Type Exists Component")
            assetexists = self.__call_asset_type_exists(type_name=type_name)
            logging.info("<<< Completed Asset Type Exists Component")
            
            if not assetexists :
                return {
                    "message" : "Asset type does not exist in the database",
                    "assettypeexists" : False,
                    "enabled" : False,
                    "type_name" : type_name
                }
            
            logging.info("<<< Initiated Asset Type Operations Component")
            self.__call_enable_asset_type(type_name=type_name)
            logging.info("<<< Completed Asset Type Operations Component")

            logging.info("!!! Completed enable asset types pipeline")
            return {
                    "message":"Asset type enabled successfully",
                    "assettypeexists" : True,
                    "enabled":True,
                    "type_name":type_name
            }
        
        except Exception as e :
            logging.error(f"!!! Error in enable asset types pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

    # get asset types
    def initiate_get_asset_types_admin_pipeline(self):
        try:
            logging.info(f"<<< Initiating get asset types pipeline")

            logging.info("<<< Initiated Asset Type Operations Component")
            asset_types = self.__call_get_asset_types()
            logging.info("<<< Completed Asset Type Operations Component")

            logging.info("!!! Completed get asset types pipeline")
            if len(asset_types) == 0:
                return {
                    "message":"No asset types found in the database",
                    "asset_types":asset_types
                }

            return {
                "message":"Asset types retrieved successfully",
                "asset_types":asset_types
            }
        
        except Exception as e :
            logging.error(f"!!! Error in get asset types pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

#--------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

# Assets 

    # get assets pipeline
    def initiate_get_assets_pipeline_admin(self):
        try:
            logging.info(f"<<< Initiating get asset types pipeline")

            logging.info("<<< Initiated Asset  Operations Component")
            assets = self.__call_get_asset()
            logging.info("<<< Completed Asset  Operations Component")

            if len(assets) == 0:
                return {
                    "message":"No assets found in the database",
                    "assets":assets
                }

            logging.info("!!! Completed get assets  pipeline")
            return {
                "message":"Assets retrieved successfully",
                "assets":assets
            }
        
        except Exception as e :
            logging.error(f"!!! Error in get asset types pipeline!!! - {CustomException(e)}")
            raise CustomException(e)
    
    # add assets pipeline
    def initiate_add_asset_pipeline(self, asset_type_name, asset_name, location, brand, purchase_year):
        try:
            logging.info(f"<<< Initiating add asset pipeline")

            todays_date = date.today()
        
            if purchase_year > todays_date.year or purchase_year < 1900:
                return {
                    "message":f"Invalid purchase year specified yeas should be between 1900 and {todays_date.year}"
                }
            
            logging.info("<<< Initiated Asset Type Exists Component")
            assetexists = self.__call_asset_type_exists(type_name=asset_type_name)
            logging.info("<<< Completed Asset Type Exists Component")

            logging.info("<<< Get asset_type_id from asset_type_name")
            asset_type_id = self.__call_get_asset_type_id(type_name=asset_type_name)
            logging.info(f" asset_type_id = {asset_type_id}")

            if not assetexists :
                return {
                    "assetexists" : False,
                    "message":"Asset type does not exist in the database"
                }
            
            logging.info("<<< Initiated Add Asset Component")
            self.__call_add_asset(asset_type_id=asset_type_id,asset_name=asset_name,location=location,
                                brand=brand,purchase_year=purchase_year)
            logging.info("<<< Completed Add Asset Component")
            
            logging.info("!!! Completed add asset pipeline")
            return {
                "assetexists":True,
                "message":"Asset added successfully"
            }
        
        except Exception as e :
            logging.error(f"!!! Error in add asset pipeline!!! - {CustomException(e)}")
            raise CustomException(e)
        
    # modify assets pipeline
    def initiate_modify_asset_pipeline(self, asset_id, asset_type_name, asset_name, location, brand, purchase_year):
        try:
            logging.info(f"<<< Initiating modify asset pipeline")
            
            todays_date = date.today()
            
            if purchase_year > todays_date.year or purchase_year < 1900:
                return {
                    "message":f"Invalid purchase year specified yeas should be between 1900 and {todays_date.year}"
                }
            
            logging.info("<<< Initiated Asset Exists Component")
            assetexist = self.__call_asset_exists(asset_id=asset_id)
            logging.info(">>> Completed Asset Exists Component")

            if not assetexist:
                return {
                    "assetExists" : False,
                    "message":f"Asset for asset id {asset_id} does not exist in the database"
                } 
            
            logging.info("<<< Initiated Asset Type Exists Component")
            assetypeexists = self.__call_asset_type_exists(type_name=asset_type_name)
            logging.info(">>> Completed Asset Type Exists Component")
            
            if not assetypeexists :
                return {
                    "assetTypeExists" : False,
                    "message":"Asset type does not exist in the database"
                }

            logging.info("<<< Get asset_type_id from asset_type_name")
            asset_type_id = self.__call_get_asset_type_id(type_name=asset_type_name)
            logging.info(f">>> asset_type_id = {asset_type_id}")
            
            logging.info("<<< Initiated Modify Asset Component")
            self.__call_modify_asset(asset_id=asset_id, asset_type_id=asset_type_id, asset_name=asset_name,
                                     location=location, brand=brand, purchase_year=purchase_year)
            
            logging.info(">>> Completed Modify Asset Component")
            
            logging.info("!!! Completed modify asset pipeline !!!")
            return {
                "assetModification":True,
                "message":"Asset modified successfully",
            }
        
        except Exception as e :
            logging.error(f"!!! Error in modify asset pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

    # soft disable asset
    def initiate_disable_asset(self,asset_id):
        try:
            logging.info("Initiating disable asset pipeline")

            logging.info("Checking if asset exists")
            assetexist = self.__call_asset_exists(asset_id=asset_id)
            if not assetexist:
                logging.info(f"Asset not found for asset id: {asset_id}")
                return {
                    "assetExists" : False,
                    "assetDisabled":False,
                    "asset_id":asset_id,
                    "message":"Asset does not exist in the database"
                }
            logging.info("Completed checking asset exists or not")
            
            logging.info("Initiated Disable Asset Operation")
            self.__call_disable_asset(asset_id)
            logging.info("Completed Disable Asset Operation")


            logging.info("!!! Completed Disable Asset Pipeline ")
            return {
                "assetExists" : True,
                "assetDisabled":True,
                "asset_id":asset_id,
                "message":"Asset disabled Sucessfully"
            }


        except Exception as e:
            logging.error(f"Error in disable asset pipeline !!! - {CustomException(e)}")
            raise CustomException(e)

    # enable asset
    def initiate_enable_asset(self,asset_id):
        try:
            logging.info("Initiating enable asset pipeline")
            
            logging.info("Checking if asset exists")
            assetexist = self.__call_asset_exists(asset_id=asset_id)
            if not assetexist:
                logging.info(f"Asset not found for asset id: {asset_id}")
                return {
                    "assetExists" : False,
                    "assetEnabled":False,
                    "asset_id":asset_id,
                    "message":"Asset does not exist in the database"
                }
            logging.info("Completed checking asset exists or not")

            logging.info("Initiated Enable Asset Operation")
            self.__call_enable_asset(asset_id)
            logging.info("Completed Enable Asset Operation")

            logging.info("!!! Completed Enable Asset Pipeline ")
            return {
                "assetExists" : True,
                "assetEnabled":True,
                "asset_id":asset_id,
                "message":"Asset enabled Sucessfully"
            }
        
        except Exception as e:
            logging.error(f"Error in enable asset pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

    # get asset details pipeline
    def initiate_get_asset_details_pipeline(self, asset_id):
        try:
            logging.info("Initiating get asset details pipeline")
            
            logging.info("Checking if asset exists")
            assetexist = self.__call_asset_exists(asset_id=asset_id)
            if not assetexist:
                logging.info(f"Asset not found for asset id: {asset_id}")
                return {
                    "assetExists" : False,
                    "message":"Asset does not exist in the database"
                }
            logging.info("Completed checking asset exists or not")
            
            logging.info("Initiating Get Asset Details Operation")
            asset_details = self.__call_get_asset_details(asset_id=asset_id)
            logging.info("Completed Get Asset Details Operation")
            
            logging.info("!!! Completed get asset details pipeline ")
            return {
                "assetExists" : True,
                "assetDetails":asset_details,
                "message":"Asset details fetched successfully"
            }
        
        except Exception as e:
            logging.error(f"Error in get asset details pipeline!!! - {CustomException(e)}")
            raise CustomException(e)
#----------------------------------------------------------------
# Transactions

    # transfer owner pipeline
    def initiate_transfer_owner_pipeline(self, asset_id, from_user_id, to_user_id): 
        try:
            logging.info("Checking if users exists for from_user_id and to_user_id")
            if not self.__call_user_exists(user_id=from_user_id) :
                logging.info(f"User not found for user_id: {from_user_id}")
                return {
                    "userExists": False,
                    "transactionStatus":False,
                    "message":f"User does not exist for user_id: {from_user_id}"
                }
            
            if not self.__call_user_exists(user_id=to_user_id) :
                logging.info(f"User not found for user_id: {to_user_id}")
                return {
                    "userExists": False,
                    "transactionStatus":False,
                    "message":f"User does not exist for user_id: {to_user_id}"
                }
            

            logging.info(f"<<< Initiating get transactions pipeline")
            if from_user_id == to_user_id :
                return {
                    "transactionStatus":False,
                    "message":"Transfer to same user is not allowed"
                }
            
            current_owner = self.__call_get_current_owner(asset_id=asset_id)
            if from_user_id != current_owner:
                return {
                    "transactionStatus":False,
                    "message":f"user_id {from_user_id} is not the owner of the asset id {asset_id}"
                }
            
            logging.info("<<< Initiating Asset Exists Component")
            assetexist = self.__call_asset_exists(asset_id=asset_id)
            logging.info("<<< Completed Asset Exists Component")
            
            if not assetexist:
                return {
                    "assetExists" : False,
                    "transactionStatus":False,
                    "message":"Asset does not exist in the database"
                }
            
            logging.info("<<< Initiated Get Transactions Component")
            message = self.__call_transfer_owner(asset_id=asset_id, from_user_id=from_user_id,to_user_id=to_user_id)
            logging.info("<<< Completed Get Transactions Component")
            
            logging.info("!!! Completed get transactions pipeline")
            return {
                "message": message if message else "Transaction Sucessfull",
                "assetExists":True,
                "transactionStatus":True
            }
        

        except Exception as e:
            logging.error(f"!!! Error in get transactions pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

    # get user transactions pipeline
    def initiate_get_user_transactions_pipeline(self, user_id):
        try:
            logging.info(f"<<< Initiating get user transactions pipeline")
            
            
            logging.info("<<< Initiated User Exists Component")
            userexists = self.__call_user_exists(user_id=user_id)
            logging.info("<<< Completed User Exists Component")
            
            if not userexists:
                return {
                    "userExists" : False,
                    "message":"User does not exist in the database"
                }
            
            logging.info("<<< Initiated Get User Transactions Component")
            transactions = self.__call_get_user_transactions(user_id=user_id)
            logging.info("<<< Completed Get User Transactions Component")
            
            logging.info("!!! Completed get user transactions pipeline")
            return {
                "userExists":True,
                "transactions":transactions
            }
        
        except Exception as e :
            logging.error(f"!!! Error in get user transactions pipeline!!! - {CustomException(e)}")
            raise CustomException(e)

#----------------------------------------------------------------
# Users

    # get user assets pipeline
    def initiate_get_user_assets_pipeline(self, user_id):
        try:
            logging.info(f"<<< Initiating get user assets pipeline")
            
            
            logging.info("<<< Initiated User Exists Component")
            userexists = self.__call_user_exists(user_id=user_id)
            logging.info("<<< Completed User Exists Component")
            
            if not userexists:
                return {
                    "userExists" : False,
                    "message":"User does not exist in the database"
                }
            
            logging.info("<<< Initiated Get User Assets Component")
            assets = self.__call_get_user_assets(user_id=user_id)
            logging.info("<<< Completed Get User Assets Component")
            
            logging.info("!!! Completed get user assets pipeline")
            return {
                "userExists":True,
                "assets":assets
            }
        
        except Exception as e :
            logging.error(f"!!! Error in get user assets pipeline!!! - {CustomException(e)}")
            raise CustomException(e)
        
    # get users details pipeline
    def initiate_get_user_details_pipeline(self):
        try:
            logging.info(f"<<< Initiating get user details pipeline")

            logging.info(f"<<< Initiating get user details component")
            users = self.__call_get_user_details()
            logging.info(f"<<< Completed get user details component")
            
            logging.info("!!! Completed get user details pipeline")
            return {
                "message": "User details retrieved successfully",
                "users": users
            }
        
        except Exception as e:
            logging.error(f"!!! Error in get user details pipeline!!! - {CustomException(e)}")
            raise CustomException(e)













