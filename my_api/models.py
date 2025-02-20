from typing import Optional
from sqlmodel import Field, SQLModel


class users(SQLModel, table=True):
    __tablename__ = "Users"
    id : Optional[int] = Field(default=None, primary_key=True)
    email: str | None = None
    username : str | None = None
    age: int | None = None
    pwd : str | None = None
    full_name: str | None = None
    disabled: bool | None = True

