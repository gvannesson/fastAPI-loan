from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .models import users
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone


SECRET_KEY = "8639fc70e75733c5e176574b59c289c89f34ef3973039ddfcd7a6bec384bbd2a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

app = FastAPI()

engine = create_engine("sqlite:///database.db")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def fake_hashed_password(password:str):
    return "fakehashed" + password

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/users/create")
async def create_user(data:dict):
    new_user=users(**data)
    new_user.pwd = pwd_context.hash((new_user.pwd))
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
    return{'message':'Utilisateur bien ajouté.'}

def fake_decode_token(token):
    return get_user(token)

def get_user(username:str):
    with Session(engine) as session:
        user = session.exec(select(users).where(users.username==username)).one_or_none()
    return user

def authenticate_user(username : str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.pwd):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Auhtenticate":"Bearer"}
    )
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exceptions
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exceptions
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exceptions
    return user

async def get_current_active_user(
    current_user: Annotated[users, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},           
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me")
async def read_users_me(current_user: Annotated[users, Depends(get_current_active_user)]):
    return current_user

@app.get("/admin/users")
async def users_list():
    with Session(engine) as session:
        user_list = session.exec(select(users)).all()
        return user_list
    

class PasswordChangeForm(BaseModel):
    previous_pwd : str
    new_pwd : str


@app.post("/auth/activation")
async def activate_account(New_password: PasswordChangeForm, current_user: Annotated[users, Depends(get_current_user)]):
    if not verify_password(New_password.previous_pwd, current_user.pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},           
        )
    with Session(engine) as session:
        user = session.exec(select(users).where(users.username==current_user.username)).one_or_none()
        user.disabled = False
        user.pwd = pwd_context.hash((New_password.new_pwd))
        session.add(user)
        session.commit()
        session.refresh(user)
    return "Compte activé et password changé"
