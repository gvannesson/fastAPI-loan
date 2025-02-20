import cloudpickle
import sklearn
import lightgbm
from app.schemas.features import Features
import pandas as pd

model = cloudpickle.load(open("./lightgbm_model.pickle", "rb"))
feature_names = ["State", "Term", "NoEmp", "UrbanRural", "cat_activites", "bank_loan_float", "SBA_loan_float", "FranchiseCode", "LowDoc", "Bank"]

def format_data(features: Features):
    data = pd.DataFrame([list(features.model_dump().values())], columns=feature_names)
    data[["State", "LowDoc", "Bank"]] = data[["State", "LowDoc", "Bank"]].astype("category")
    print(data.dtypes)
    return data

