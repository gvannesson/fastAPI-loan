from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class PasswordChangeForm(BaseModel):
    previous_pwd : str
    new_pwd : str