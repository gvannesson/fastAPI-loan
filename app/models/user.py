from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    id : Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(unique=True, max_length=255)
    password: str = Field(max_length=255)
    email: Optional[str] = Field(max_length=255)
    disabled: Optional[bool] = Field(default=True)
    role: int
    is_active: Optional[bool] | None = False
