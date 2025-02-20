from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.user import User
from app.db.session import get_session
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_handler import verify_token
from typing import Annotated
from jwt import decode
from jwt.exceptions import InvalidTokenError
from app.schemas.auth import TokenData
from app.db.transactions import get_user
from app.core.config import SECRET_KEY, ALGORITHM


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
        
    user = get_user(token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user : Annotated[User, Depends(get_current_user)]
):   
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.get("/admin/users")
async def user_list(user: Annotated[User, Depends(get_current_active_user)], session : Annotated[Session, Depends(get_session)]):
    if user.role != 1:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_list = session.exec(select(User)).all()
    return user_list

