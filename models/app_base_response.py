from pydantic import BaseModel


class AppBaseResponse(BaseModel):

    http_code: int
    message: str

    def to_dict(self) -> dict:
        """Return the dictionary representation of the model using alias."""

        _dict = self.model_dump(by_alias=True)
        return _dict
