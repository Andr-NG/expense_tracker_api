from typing import List
from models.app_base_response import AppBaseResponse
from models.categories import Categories


class GetCategoriesResponse(AppBaseResponse):

    data: List[Categories] | None = None
