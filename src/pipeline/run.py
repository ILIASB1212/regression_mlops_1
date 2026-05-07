import pandas as pd

from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation









if __name__=="__main__":
    config=ConfigurationManager()
    data_ingestion_config=config.get_data_ingestion_config()
    data_ingestion=DataIngestion(config=data_ingestion_config)
    data_ingestion.doownload_data()
    data_validation_config=config.get_data_validation_config()
    data_validation=DataValidation(data_validation_config)
    data_validation.validate_all_columns()
    data_transformation_config=config.get_data_transformation_config()
    data_trasformation=DataTransformation(data_transformation_config)
    data_trasformation.split_data_as_train_test()




