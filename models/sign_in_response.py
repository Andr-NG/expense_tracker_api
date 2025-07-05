from pydantic import Field
from models.app_base_response import AppBaseResponse


class SignInResponse(AppBaseResponse):

    user_id: int = Field(..., description="User ID")
    token: str = Field(..., description="User JWT")
    
