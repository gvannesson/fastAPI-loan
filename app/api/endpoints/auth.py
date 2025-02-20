from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import Token
from app.utils.jwt_handler import create_access_token
from app.db.transactions import authenticate_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
    )    
    return Token(access_token=access_token, token_type="bearer")
