from pydantic import BaseModel, EmailStr, StrictInt


class UserToken(BaseModel):
    email: EmailStr
    user_id: StrictInt
    is_active: bool
    iat: int
    exp: int