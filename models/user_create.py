from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):

    # username: str = Field(..., min_length=1, max_length=16, description="Username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=5, max_length=16, description="User password")

    model_config = ConfigDict(
        validate_assignment=True,
    )