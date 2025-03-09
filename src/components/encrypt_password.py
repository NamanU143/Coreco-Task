import sys
from src.exception import CustomException
from src.logger import logging
from fastapi import HTTPException
import bcrypt

class EncryptPassword:
    """
    Class for encrypting user password.
    """
    def __init__(self,password):
        try:
            self.password = password
        except CustomException as e:
            logging.error(f"Error initializing password encryption: {e}")
            raise e

    def __encrypt_password(self):
        """
        Encrypts the user password using a secure encryption algorithm.
        """
        try:
            log_rounds = 12  # here we can can adjust this value based on your security requirements
            salt = bcrypt.gensalt(rounds=log_rounds)
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), salt)
            hashed_password_str = hashed_password.decode('utf-8')
            
            return hashed_password_str
        
        except Exception as e:
            logging.error(f"Error encrypting password: {e}")
            raise HTTPException(status_code=500, detail="Password encryption failed")
        

    def initiate_encryption(self):
        """
        Initiates the password encryption process.
        """
        try:
            encrypted_password = self.__encrypt_password()
            logging.info(f"Encrypted password: {encrypted_password}")
            return encrypted_password
        
        except HTTPException as e:
            logging.error(f"Error initiating encryption: {e}")
            raise HTTPException(status_code=500, detail=e.detail)

    

# defining the number of rounds for salt generation (log_rounds)
# generating a salt with the specified numbr of rounds
# here we are hashing our users password using the generated saltl
# converting the hashed password to a string
