from typing import Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Transaction(BaseModel):

    transaction_id: str | None = Field(
        default=None, description="Unique transaction ID"
    )
    amount: float = Field(default=0, gt=0, description="Transaction amount")
    type: Literal["income", "expense"]
    category_id: int = Field(..., description="Transaction category id")
    date: str | None = Field(default=None, description="Added dated in DD.MM.YYYY")
    description: str | None = Field(default=None, description="Transaction description")

    @field_validator("date")
    @classmethod
    def is_correct_date_format(cls, value: str):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
            return value

        except ValueError:
            raise ValueError("date format should be MM.DD.YYYY")