from src.config.configuration import ModelTrainerConfig
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.utils.common import create_directorie,save_model
from sklearn.metrics import accuracy_score
from src.loging.logger import logging
from xgboost import XGBClassifier







class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config=config
    def load_data(self):
        try:
            
            data=pd.read_csv(self.config.training_set)
            create_directorie(self.config.model_dir)

            y=data[self.config.target_columns]
            x=data.drop(columns=[self.config.target_columns,self.config.droped_column])
            self.strings=list(x.select_dtypes(include="object").columns)
            self.intigers=list(x.select_dtypes(exclude="object").columns)

            self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(x,y,test_size=self.config.test_size)

            
            return self.x_train,self.x_test,self.y_train,self.y_test,self.strings,self.intigers
        except Exception as e:
            logging.error(f"Error occurred while downloading data: {e}")
            raise ConnectionError(f"Failed to download data  {e}")


    def initialise_model_trainer(self):
        

        # Build ColumnTransformer
        preprocessor = ColumnTransformer([
            # Numeric: impute mean/median, then scale
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),  # or 'mean'
                ('scaler', StandardScaler())
            ]), self.intigers),
            
            # Categorical: impute with most frequent, then one-hot encode
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ]), self.strings)
        ])

        # Create full pipeline (preprocessing + model)
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression())
        ])

        # Fit and predict
        pipeline.fit(self.x_train,self.y_train)   # example target
        save_model(pipeline,self.config.model_path)
        predictions = pipeline.predict(self.x_test)
        metric=accuracy_score(predictions,self.y_test)
        logging.info(f"traing model accurecy is {metric}")