from typing import Optional
from sqlmodel import Field, SQLModel


class users(SQLModel, table=True):
    __tablename__ = "Users"
    id : Optional[int] = Field(default=None, primary_key=True)
    username : str

# class loan_requests(SQLModel):
#     pass