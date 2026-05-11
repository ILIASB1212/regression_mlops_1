from fastapi import FastAPI
from pydantic import BaseModel
from src.utils.common import load_model,read_yaml
import pandas as pd

yaml_file=read_yaml("config/config.yaml")
apps = FastAPI()

model = load_model(yaml_file.model_trainer.model_path)

class CreditRequest(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    Saving_accounts: str
    Checking_account: str
    Credit_amount: int
    Duration: int
    Purpose: str

@apps.post("/predict")
def predict(request: CreditRequest):
    df = pd.DataFrame([request.model_dump()])
    df.rename(columns={
        'Saving_accounts': 'Saving accounts',
        'Checking_account': 'Checking account',
        'Credit_amount': 'Credit amount'
    }, inplace=True)
    prediction = model.predict(df)
    return {"risk": "good" if prediction[0] == 1 else "bad"}


