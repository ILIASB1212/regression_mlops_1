from src.entity.config_entity import DataTransformationConfig
from src.loging.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.common import create_directorie
import sys
from src.exceptions.custom_exceptions import CustomException

class DataTransformation:
    def __init__(self,config:DataTransformationConfig):
          self.config=config

    def split_data_as_train_test(self):
        try:
            data=pd.read_csv(self.config.local_data_file)

            create_directorie(self.config.root_dir_train)

            logging.info(f"created file at {self.config.root_dir_train}")

            create_directorie(self.config.root_dir_test)

            logging.info(f"created file at {self.config.root_dir_test}")

            train,test=train_test_split(data,
                                        random_state=self.config.random_state,
                                        test_size=self.config.test_size)
                    
            logging.info(f"created file at train and test set ")

            train.to_csv(self.config.train_dir,index=False,header=True)

            logging.info(f"saved trainoing set file at {self.config.train_dir}")
            logging.info(f"traing set size is {train.shape}")

            test.to_csv(self.config.test_dir,index=False,header=True)

            logging.info(f"saved test set file at {self.config.test_dir}")
            logging.info(f"test set size is {test.shape}")
        except Exception as e:
            logging.error(f"error in data transformation class ,error content {e}")
            raise CustomException(f"error in data transformation class error content {e}",sys)

