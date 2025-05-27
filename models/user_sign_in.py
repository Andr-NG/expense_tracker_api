from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSignIn(BaseModel):

    # username: str | None = None, Field(..., min_length=1, max_length=16, description="Username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=5, max_length=16, description="User password")

    model_config = ConfigDict(
        validate_assignment=True,
    )
