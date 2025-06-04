from typing import Literal
from pydantic import BaseModel, Field, StrictInt


class CreateTransaction(BaseModel):

    user_id: StrictInt = Field(..., description="User ID")
    amount: StrictInt = Field(..., gt=0, description="Transaction amount")
    type: Literal["income", "expense"]
    category: str = Field(..., description="Transaction category")
    date: str = Field(..., description="Added dated")
    description: str | None = None