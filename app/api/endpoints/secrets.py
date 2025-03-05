from fastapi import APIRouter, Depends
from app.models.user import User
from app.db.session import get_session
from typing import Annotated
from sqlmodel import Session
from app.core.security import pwd_context

router = APIRouter()

@router.post("/secret/users", include_in_schema=False)
async def create_user(data:dict, session: Annotated[Session, Depends(get_session)]):
    try:            
        new_user=User(**data)      
        new_user.password = pwd_context.hash(new_user.password)
        print(new_user)        
        session.add(new_user)
        session.commit()
        return{'message':'User successfully created.'}
    except:
        return {"message": 'Invalid datas. The user was not created.'}