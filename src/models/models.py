from sqlalchemy import Column, Integer, String,Enum,Boolean,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship
from src.logger import logging
from src.configuration.mysql_connection import DatabaseConnection
from typing import Optional


db_conn = DatabaseConnection()
Base = db_conn.Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum("Admin", "User", name="role"), nullable=False, default="User")
    password = Column(String(255), nullable=False)

    def __init__(self, name, email,password,role:Optional[str]=None,id:Optional[int]=None):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.password = password

    def __repr__(self):
        return f"id={self.id}, name={self.name}, email={self.email}, role={self.role},password={self.password}"

    # def __str__(self):
    #     return f"User: {self.name} ({self.email}) - Role: {self.role}"

class AssetTypes(Base):
    __tablename__ = 'asset_types'
    
    asset_type_id = Column(Integer, nullable=False,primary_key=True,autoincrement=True,index=True)
    type_name = Column(String(100),unique=True,nullable=False)
    is_active = Column(Boolean,default=True)
    # id int primary key auto_increment,
    # type_name VARCHAR(100) unique not null,
    # is_active boolean default true

    def __init__(self,type_name:str,is_active:Optional[bool]=None,id:Optional[int]=None):
        self.id = id
        self.type_name = type_name
        self.is_active = is_active

    def __repr__(self):
        return f"id={self.id} ,type_name={self.type_name} ,is_active={self.is_active}"
    
class Asset(Base):
    __tablename__ = 'assets'
    
    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.asset_type_id', ondelete='CASCADE'))
    asset_name = Column(String(255))
    location = Column(String(255))
    brand = Column(String(255))
    purchase_year = Column(Integer)   # change after ward
    is_active_asset = Column(Boolean, default=True)
    current_owner = Column(Integer, ForeignKey('users.id', ondelete='SET DEFAULT'), nullable=False, default=1)  # default value to 1 for admin
    purchase_date = Column(DateTime)

    def __init__(self, asset_type_id: int, asset_name: str, location: str, brand: str, purchase_year: Integer,purchase_date:Optional[DateTime], 
                 is_active_asset: Optional[bool] = None,  current_owner: Optional[int] = 1, asset_id: Optional[int] = None):
        self.asset_id = asset_id
        self.asset_type_id = asset_type_id
        self.asset_name = asset_name
        self.location = location
        self.brand = brand
        self.purchase_year = purchase_year
        self.is_active_asset = is_active_asset
        self.current_owner = current_owner
        self.purchase_date = purchase_date
        

    
    def __repr__(self):
        return f"asset_id={self.asset_id}, asset_type_id={self.asset_type_id}, asset_name={self.asset_name}, location={self.location}, brand={self.brand}, purchase_year={self.purchase_year}, is_active={self.is_active_asset}, current_owner={self.current_owner}"
    
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_date = Column(DateTime, default=func.now())


    def __init__(self, asset_id: int, from_user_id: int, to_user_id: int):
        self.asset_id = asset_id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    def __repr__(self):
        return f"asset_id={self.transaction_id}, asset_id={self.asset_id}, from_user_id={self.from_user_id}, to_user_id={self.to_user_id}, transaction_date={self.transaction_date}"