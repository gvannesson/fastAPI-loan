from app.utils.model_handler import model, format_data
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.features import Features
import pandas as pd
from app.db.transactions import new_loan_request
from typing import Annotated
from app.api.endpoints.users import get_current_user_id, get_current_active_user
from app.models.loan_requests import Loan_Request
from app.models.user import User
from app.db.session import Session, get_session
from sqlmodel import select

router = APIRouter()

@router.post("/loans/predict")
async def predict(features: Features, user_id: Annotated[int, Depends(get_current_user_id)]):
    data = format_data(features)
    # print(type(data))
    # print(model.feature_name_)  
    try:
        result = model.predict(data)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid datas for prediction.",
            headers={"WWW-Authenticate": "Bearer"},                
        )    
    new_loan_request(result=result.tolist()[0], user_id=user_id)
    return result.tolist()


@router.get("/loans/history")
async def prediction_history(user: Annotated[User, Depends(get_current_active_user)],user_id: Annotated[User, Depends(get_current_user_id)], session : Annotated[Session, Depends(get_session)]):
    if user.role != 0:
        prediction_list = session.exec(select(Loan_Request)).all()
    else:
        prediction_list = session.exec(select(Loan_Request).where(Loan_Request.user_id == user_id)).all()
    return prediction_list
