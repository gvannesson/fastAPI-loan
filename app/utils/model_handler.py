import cloudpickle
import sklearn
import lightgbm
from app.schemas.features import Features
import pandas as pd

metadata = cloudpickle.load(open("./lightgbm_model.pickle", "rb"))
model = metadata["model"]
categorical_features = metadata["categorical_features"]
feature_names = ["State", "Term", "NoEmp", "UrbanRural", "cat_activites", "bank_loan_float", "SBA_loan_float", "FranchiseCode", "LowDoc", "Bank"]

def format_data(features: Features):
    data = pd.DataFrame([list(features.model_dump().values())], columns=feature_names)
    for col in categorical_features:
        data[col] = data[col].astype("category").cat.codes 
    return data

