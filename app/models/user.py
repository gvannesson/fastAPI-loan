from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    id : Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(unique=True)
    password: str
    email: Optional[str]
    disabled: Optional[bool] = Field(default=True)
    role: int
    is_active: Optional[bool] | None = False
