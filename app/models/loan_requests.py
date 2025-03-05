from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.user import User
from datetime import datetime

class Loan_Request(SQLModel, table=True):
    
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id", ondelete='CASCADE')
    result: str
    date: datetime =Field(default_factory=datetime.now)