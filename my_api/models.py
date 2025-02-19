from typing import Optional
from sqlmodel import Field, SQLModel


class users(SQLModel, table=True):
    __tablename__ = "Users"
    id : Optional[int] = Field(default=None, primary_key=True)
    username : str
    age: Optional[int]
    hashed_password: str = Field(default="")
    email: Optional[str]
    disabled: Optional[bool] = Field(default=False)

# class loan_requests(SQLModel):
#     pass