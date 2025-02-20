from app.utils.model_handler import model, format_data
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.features import Features
import pandas as pd

router = APIRouter()

@router.post("/loans/predict")
async def predict(features: Features):
    data = format_data(features)
    print(type(data))
    result = model.predict(data)
    try:
        pass
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid datas for prediction.",
            headers={"WWW-Authenticate": "Bearer"},                
        )    
    return result