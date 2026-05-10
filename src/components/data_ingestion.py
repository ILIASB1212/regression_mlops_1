from src.entity.config_entity import DataIngestionConfig
import pandas as pd  
from src.loging.logger import logging

import sys
from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src.exceptions.custom_exceptions import CustomException



class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config


    def doownload_data(self):
        try:
            data=pd.read_csv(self.config.dataset_download_url)
            data.to_csv(self.config.load_dataset_lacation,index=False,header=True)
            logging.info(f"Data downloaded from {self.config.dataset_download_url} and saved to {self.config.load_dataset_lacation}")
        except Exception as e:
            logging.error(f"error in data ingestion class ,error content {e}")
            CustomException(f"error in data ingestion class error content {e}",sys)
        

        







