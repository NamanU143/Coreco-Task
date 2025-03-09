from src.pipeline import Pipeline
from src.logger import logging


pipeline = Pipeline()

result = pipeline.initiate_registration_pipeline(name="Kunal",email="admin2@gmail.com",password="12345")
logging.info(result)