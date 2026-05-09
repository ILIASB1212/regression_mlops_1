from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.utils.common import read_yaml, create_directorie
from src.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,ModelEvaluationConfig

from src.loging.logger import logging
from sklearn.model_selection import train_test_split

import pandas as pd







class ConfigurationManager:
    def __init__(self,config_file_path=CONFIG_FILE_PATH,
                 params_file_path=PARAMS_FILE_PATH,
                 schema_file_path=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)


        create_directorie(self.config.artifacts_root)
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            create_directorie(self.config.dataingestion.root_dir)
            data_ingestion_config=DataIngestionConfig(
                root_dir=self.config.dataingestion.root_dir,
                dataset_download_url=self.config.dataingestion.source_URL,
                load_dataset_lacation=self.config.dataingestion.local_data_file,
                upload_dataset_location=self.config.dataingestion.unzip_dir
            )

            return data_ingestion_config
        
        except Exception as e:
            raise e



    def get_data_validation_config(self) -> DataValidationConfig:


        create_directorie(self.config.data_validation.status_folder)

        data_validation_config=DataValidationConfig(
            root_dir=self.config.data_validation.root_dir,
            local_data_file=self.config.data_validation.local_data_file,
            status_folder=self.config.data_validation.status_folder,
            status_file=self.config.data_validation.status_file,
            schemas=self.schema.COLUMNS


        )
        return data_validation_config
        

    def get_data_transformation_config(self)->DataTransformationConfig:


        data_transformation_config=DataTransformationConfig(
            local_data_file=self.config.data_transformation.local_data_file,
            root_dir_train=self.config.data_transformation.root_dir_train,
            root_dir_test=self.config.data_transformation.root_dir_test,
            train_dir=self.config.data_transformation.train_dir,
            test_dir=self.config.data_transformation.test_dir,
            test_size=self.config.data_transformation.test_size,
            random_state=self.config.data_transformation.random_state
        )
        return data_transformation_config
    

    def get_model_trainer_config(self)->ModelTrainerConfig:
        model_trainer_config=ModelTrainerConfig(
            training_set=self.config.model_trainer.training_set,
            droped_column=self.config.model_trainer.droped_column,
            target_columns=self.config.model_trainer.target_columns,
            test_size=self.config.model_trainer.test_size,
            model_dir=self.config.model_trainer.model_dir,
            model_path=self.config.model_trainer.model_path,
        )
        return model_trainer_config
    


    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        model_evaluation_config=ModelEvaluationConfig(
            model_path=self.config.model_evaluation.model_path,
            test_set=self.config.model_evaluation.test_set,
            droped_column=self.config.model_evaluation.droped_column,
            target_columns=self.config.model_evaluation.target_columns,
        )
        return model_evaluation_config

        
        

        

