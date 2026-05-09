from src.entity.config_entity import DataValidationConfig
from src.loging.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.common import read_yaml, create_directorie





class DataValidation:
    def __init__(self,config:DataValidationConfig):
        self.config=config
    

    def validate_all_columns(self)-> bool:
        try:
            validation_status = None
            data = pd.read_csv(self.config.local_data_file)
            all_cols = list(data.columns)

            all_schema = self.config.schemas.keys()

            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.status_file, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                        logging.info("data validated sussesfuly")
                else:
                    validation_status = True
                    with open(self.config.status_file, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                        logging.error("error data validation --verify your data--")

            return validation_status

        except Exception as e:
            logging.error(f"Error occurred while downloading data: {e}")
            raise ConnectionError(f"Failed to download data  {e}")