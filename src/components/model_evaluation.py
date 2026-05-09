from src.config.configuration import ModelEvaluationConfig
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.utils.common import create_directorie,load_model
from sklearn.metrics import accuracy_score
from src.loging.logger import logging






class ModelEvaluation:
    def __init__(self,config:ModelEvaluationConfig):
        self.config=config
    def evaluate_model(self):
        try:
            
            data=pd.read_csv(self.config.test_set)
            model_path=self.config.model_path
            model=load_model(model_path)


            y=data[self.config.target_columns]
            x=data.drop(columns=[self.config.target_columns,self.config.droped_column])
            predict=model.predict(x)
            metric=accuracy_score(predict,y)
            logging.info(f"testing model accuracy  accurecy is ----> {metric}")



        except Exception as e:
            logging.error(f"Error occurred while downloading data: {e}")
            raise ConnectionError(f"Failed to download data  {e}")


    