from app.db.session import get_session
from sqlmodel import Session
from fastapi import Depends
from sqlmodel import select
from app.models.user import User
from app.models.loan_requests import Loan_Request
from app.core.security import verify_password
from app.db.session import engine

def get_user(username: str, session: Session = Depends(get_session)):    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).one_or_none()    
    return user

def authenticate_user(username:str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def new_loan_request(result: str, user_id: int):
    loan = Loan_Request(user_id=user_id, result=result)
    with Session(engine) as session:
        session.add(loan)
        session.commit()
        session.refresh(loan)
    
    pass
    
