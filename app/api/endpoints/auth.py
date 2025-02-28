from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import Token, PasswordChangeForm
from app.utils.jwt_handler import create_access_token
from app.db.transactions import authenticate_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from .users import get_current_user
from app.core.security import verify_password, pwd_context
from app.db.session import Session, engine
from sqlmodel import select

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


@router.post("/auth/activation")
async def activate_account(New_password: PasswordChangeForm, current_user: Annotated[User, Depends(get_current_user)]):
    if not verify_password(New_password.previous_pwd, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},           
        )
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username==current_user.username)).one_or_none()
        user.disabled = False
        user.password = pwd_context.hash((New_password.new_pwd))
        session.add(user)
        session.commit()
        session.refresh(user)
    return "Compte activé et password changé"