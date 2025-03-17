# Following is the code of logging without initializing any setup logger function 
# due to following code we can directly use the logging .


import logging
import os
from datetime import datetime

log_folder = os.path.join(os.getcwd(), "logs")
os.makedirs(log_folder, exist_ok=True)
log_file_path = os.path.join(log_folder, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")

# Configure logging globally
logging.basicConfig(
    level=logging.DEBUG,  # Set log level
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),  # Log to file
        # logging.StreamHandler()  # Log to console
    ]
)
