from fastapi import FastAPI ,Body,Query
from fastapi import HTTPException
from src.exception import CustomException
from pydantic import BaseModel
from src.pipeline import Pipeline
from src.logger import logging
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
pipeline = Pipeline()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/")
# def root():
#     return {"message": "Asset Management API is running!"}

class RegisterUserData(BaseModel):
    name: str
    email: str
    password: str

class LoginUserData(BaseModel):
    email:str
    password: str

class ModifyAssetType(BaseModel):
    type_name: str
    new_type_name: Optional[str]

class AddAssetType(BaseModel):
    type_name:str

class AddAsset(BaseModel):
    asset_type_name:str
    asset_name:str
    location:str
    brand:str
    purchase_year:int

class ModifyAsset(BaseModel):
    asset_id:int
    asset_type_name:Optional[str]=None
    asset_name: Optional[str]
    location: Optional[str]
    brand: Optional[str]
    purchase_year: Optional[int]

class TransferAsset(BaseModel):
    asset_id: int
    from_user_id: int
    to_user_id: int



@app.post("/register")
async def register_user(data:RegisterUserData):
    """
    Args:
        email,name,password
    Returns:
        dict: Response from registration pipeline.
    Raises:
        CustomException: If an error occurs during the pipeline execution.
    """
    try:
        # Initiate the pipeline with the provided email
        response = pipeline.initiate_registration_pipeline(name=data.name,email=data.email,password=data.password)
        return response
    except HTTPException as e:
        logging.info(f"Error While Registration of User - {CustomException(e)}")
        return {"message": str(e.detail)}
    
@app.post("/login")
async def login_user(data:LoginUserData):
    """
    Args :
        email,password
    Returns :
        dict : Response from the login pipeline.
    Raises:
        CustomException: If an error occurs during the pipeline execution.
    """
    try:


        # Initiate the pipeline with the provided email
        response = pipeline.initiate_login_pipeline(email=data.email,password=data.password)
        # While login if user is genral user then redirect him to the general user dashboard <general_user_dashboard.html>
        # While login if user is admin then redirect him to the Admin dashboard  <admin_dashboard.html>
        return response
    except HTTPException as e:
        logging.info(f"Error While Registration of User - {CustomException(e)}")
        return {"message": str(e.detail)}


# ------------------------------------------------------------------------------------------------
@app.post("/admin/add_asset_types")
async def add_asset_types(data:AddAssetType= Body(...)):
    """
    Args : asset_type_name
    Returns : dict : response from asset_types_pipeline
    """
    try:
        response = pipeline.initiate_add_asset_type_pipeline(asset_type_name=data.type_name)
        return response
    except HTTPException as e:
        logging.info(f"Error While Adding Asset Type - {CustomException(e)}")
        return {"message": str(e.detail)}
    
@app.patch("/admin/modify_asset_types")
async def modify_asset_types(data:ModifyAssetType = Body(...)):
    """
    Args : asset_type_id, new_name
    Returns : dict : response from asset_types_pipeline
    """
    try:
        response = pipeline.initiate_modify_asset_type_pipeline(type_name=data.type_name, new_type_name=data.new_type_name)
        return response
    except HTTPException as e:
        logging.info(f"Error While Modifying Asset Type - {CustomException(e)}")
        return {"message": str(e.detail)}
    
@app.delete("/admin/soft_delete_asset_type/{type_name}")
async def soft_delete_asset_type(type_name:str):
    """
    Args :param - in link type name
    Returns : dict : response from soft_telete_pipeline
    """
    try:
        response = pipeline.initiate_soft_disable_asset_type_pipeline(type_name=type_name)
        return response
    except HTTPException as e:
        logging.info(f"Error While Soft Deleting Asset Type - {CustomException(e)}")
        return {"message": str(e.detail)}

@app.patch("/admin/enable_asset_type/{type_name}")
async def enable_asset_type(type_name:str):
    """
    Args : param - in link type name
    Returns : dict : response from enable_pipeline
    """
    try:
        response = pipeline.initiate_enable_asset_types_admin_pipeline(type_name=type_name)
        return response
    except HTTPException as e:
        logging.info(f"Error While Enabling Asset Type - {CustomException(e)}")
        return {"message": str(e.detail)}

@app.get("/admin/get_asset_types")
async def get_asset_types():
    """
    Returns : dict : response from asset_types_pipeline
    """
    try:
        response = pipeline.initiate_get_asset_types_admin_pipeline()
        return response
    except HTTPException as e:
        logging.info(f"Error While Getting Asset Types - {CustomException(e)}")
        return {"message": str(e.detail)}

# --------------------------------------------------------------------------------------------------------------------------------

@app.get("/admin/get_assets")
async def get_assets():
    """
    Returns : dict : response from assets_pipeline
    """
    try:
        response = pipeline.initiate_get_assets_pipeline_admin()
        return response
    except HTTPException as e:
        logging.info(f"Error While Getting Asset Types - {CustomException(e)}")
        return {"message": str(e.detail)}
    
@app.post("/admin/add_assets")
async def add_assets(data:AddAsset=Body(...)):
    """
    Args : asset_type_id, asset_name, description, quantity, price
    Returns : dict : response from assets_pipeline
    """
    try:
        response = pipeline.initiate_add_asset_pipeline(asset_type_name=data.asset_type_name,asset_name=data.asset_name
                                                        ,location=data.location, brand=data.brand,purchase_year=data.purchase_year)

        return response
    except HTTPException as e:
        logging.info(f"Error While Adding Asset Types - {CustomException(e)}")
        return {"message": "Error while adding asset"}

@app.patch("/admin/modify_assets")
async def modify_assets(data:ModifyAsset=Body(...)):
    try:
        response = pipeline.initiate_modify_asset_pipeline(asset_id=data.asset_id,asset_type_name=data.asset_type_name,
                                                           asset_name=data.asset_name,location=data.location,brand=data.brand,
                                                           purchase_year=data.purchase_year)
        return response
    except HTTPException as e:
        logging.info(f"Error While Modifying Asset Types - {CustomException(e)}")
        return {"message": "Error while modifying asset"}

@app.delete("/admin/disable_asset/{asset_id}")
async def disable_asset(asset_id:int):
    """
    Args: asset_id: The id of the asset
    Returns : dict : response from disable_asset_pipeline

    """
    try:
        response = pipeline.initiate_disable_asset(asset_id=asset_id)
        return response
    except HTTPException as e:
        logging.info(f"Error while Disabling asset {CustomException(e)}")
        return{"message": str(e.detail)}

@app.patch("/admin/enable_asset/{asset_id}")
async def enable_asset(asset_id):
    try:
        response = pipeline.initiate_enable_asset(asset_id=asset_id)
        return response
    except HTTPException as e :
        logging.info(f"Error while Enabling asset {CustomException(e)}")
        return {"message": str(e.detail)}

# --------------------------------------------------------------------------------------------------------------------------------

@app.get("/get_user_assets/{user_id}")
async def get_user_assets(user_id):
    """

    Args: user_id: The id of the user
    Returns : dict : response from get_user_assets_pipeline
    """
    try:
        response = pipeline.initiate_get_user_assets_pipeline(user_id=user_id)
        return response
    except HTTPException as e:
        logging.info(f"Error while Getting User Assets {CustomException(e)}")
        return {"message": str(e.detail)}

@app.put("/transfer_owner/")
async def transfer_owner(data:TransferAsset=Body(...)):
    """
    Args: from_user_id, to_user_id: The ids of the users
    Returns : dict : response from transfer_asset_pipeline
    """
    try:
        response = pipeline.initiate_transfer_owner_pipeline(asset_id=data.asset_id,from_user_id=data.from_user_id, to_user_id=data.to_user_id)
        return response
    except HTTPException as e:
        logging.info(f"Error while Transferring Asset {CustomException(e)}")
        return {"message": str(e.detail)}

# --------------------------------------------------------------------------------------------------------------------------------
@app.get("/get_users")
async def get_users():
    try:
        response = pipeline.initiate_get_user_details_pipeline()
        return response
    except HTTPException as e:
        logging.info(f"Error while Getting Users {CustomException(e)}")
        return {"message": str(e.detail)}

@app.get("/get_user_transactions/{user_id}")
async def get_user_transactions(user_id):
    try:
        response = pipeline.initiate_get_user_transactions_pipeline(user_id=user_id)
        return response
    except HTTPException as e:
        logging.info(f"Error while Getting User Transactions {CustomException(e)}")
        return {"message": str(e.detail)}

@app.get("/admin/get_asset_details/{asset_id}")
async def get_asset_details(asset_id):
    try:
        response = pipeline.initiate_get_asset_details_pipeline(asset_id=asset_id)
        return response
    except HTTPException as e:
        logging.info(f"Error while Getting Asset Details {CustomException(e)}")
        return {"message": str(e.detail)}
    

if __name__ == "__main__":
    app.debug = True
    uvicorn.run(app, host="0.0.0.0", port=3000)