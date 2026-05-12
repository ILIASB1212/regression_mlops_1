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
from sklearn.metrics import accuracy_score,f1_score
from src.loging.logger import logging
import sys
from xgboost import XGBClassifier
from src.exceptions.custom_exceptions import CustomException
import mlflow
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import dagshub










class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config=config
        
    def load_data(self):
        try:
            
            data=pd.read_csv(self.config.training_set)
            create_directorie(self.config.model_dir)

            y=data[self.config.target_columns]
            y=np.where(y=="good",1,0)
            logging.info(f"the first 5 value of encoding numerical target is {y[:5]}")
            x=data.drop(columns=[self.config.target_columns,self.config.droped_column])
            self.strings=list(x.select_dtypes(include="object").columns)
            self.intigers=list(x.select_dtypes(exclude="object").columns)

            self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(x,y,test_size=self.config.test_size)

            
            return self.x_train,self.x_test,self.y_train,self.y_test,self.strings,self.intigers
        except Exception as e:
            logging.error(f"Error occurred while downloading data in model trainer class : {e}")
            raise CustomException(f"Failed to download data   {e}")


    def initialise_model_trainer(self):
        
        try:
            # Build ColumnTransformer

            preprocessor = ColumnTransformer([
                ('num', Pipeline([
                    ('imputer', SimpleImputer(strategy='median')),  
                    ('scaler', StandardScaler())
                ]), self.intigers),
                
                ('cat', Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
                ]), self.strings)
            ])

            # Create full pipeline (preprocessing + model)
            dagshub.init(repo_owner='ILIASB1212', repo_name='regression_mlops_1', mlflow=True)
            mlflow.set_experiment("mlflow bank ")
            models=[GradientBoostingClassifier,RandomForestClassifier,LogisticRegression,XGBClassifier]
            report={}
            pipelines={}

            for model in models:
                ml_model=model()
                model_name = ml_model.__class__.__name__

                pipeline = Pipeline([
                    ('preprocessor', preprocessor),
                    ('classifier', ml_model)
                ])

                
                with mlflow.start_run():
                    # fit the model/pipeline
                    pipeline.fit(self.x_train,self.y_train)   
                    # predict and test accuracy
                    predictions = pipeline.predict(self.x_test)
                    accuracy=accuracy_score(predictions,self.y_test)
                    f1=f1_score(predictions,self.y_test)
                    #save the models scores and names in the 
                    report[model_name]=f1
                    pipelines[model_name] = pipeline

                    logging.info(f"traing model: {model_name} accurecy is {accuracy}")
                    logging.info(f"traing model: {model_name} f1_score is {f1}")
                    # save models performense and atributes
                    mlflow.sklearn.log_model(sk_model=pipeline, artifact_path="model")
                    # save models params
                    mlflow.log_params({"model_name":model_name,
                                       
                                    "model_params":ml_model.get_params()})
                    # save models performense
                    mlflow.log_metrics({"accuracy":accuracy,
                                        "f1_score":f1})

            logging.info(f"models report == {report}")

            # save the best models performence
            best_model_name = max(report, key=report.get)
            # save the best model for test set
            save_model(pipelines[best_model_name], self.config.model_path)
            logging.info(f"Best model saved: {best_model_name} | F1: {report[best_model_name]:.4f}")
        except Exception as e:
            logging.error(f"error in mode trainer class error content {e}")
            raise CustomException(f"error in mode trainer class error content {e}",sys)