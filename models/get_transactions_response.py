from typing import List
from models.app_base_response import AppBaseResponse
from models.transaction import Transaction


class GetTransactionsResponse(AppBaseResponse):

    data: List[Transaction] | None = None
    count: int

