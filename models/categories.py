from typing import Literal
from pydantic import BaseModel, Field


class Categories(BaseModel):

    id: int = Field(default=None, description="Category ID")
    type: Literal["income", "expense"]
    name: str = Field(..., description="Category name")
    date: str | None = Field(default=None, description="Added dated in DD.MM.YYYY")
    description: str | None = Field(default=None, description="Category description")

    class Config:
        exclude_none = True
