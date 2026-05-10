from src.config.configuration import ModelEvaluationConfig
from src.utils.common import load_model
import pandas as pd
from sklearn.metrics import accuracy_score,f1_score
from src.loging.logger import logging
import numpy as np






class ModelEvaluation:
    def __init__(self,config:ModelEvaluationConfig):
        self.config=config
    def evaluate_model(self):
        try:
            
            data=pd.read_csv(self.config.test_set)
            model_path=self.config.model_path
            model=load_model(model_path)


            y=data[self.config.target_columns]
            y=np.where(y=="good",1,0)
            x=data.drop(columns=[self.config.target_columns,self.config.droped_column])
            predict=model.predict(x)
            accuracy=accuracy_score(predict,y)
            logging.info(f"testing model accuracy  accurecy is ----> {accuracy}")
            f1=f1_score(predict,y)
            logging.info(f"testing model f1_score is {f1}")

            from src.exceptions.custom_exceptions import CustomException
            import sys
        except Exception as e:
            logging.error(f"error in model evaluation class ,error content {e}")
            raise CustomException(f"error in model evaluation class error content {e}",sys)
