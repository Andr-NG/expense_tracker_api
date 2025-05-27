from models.app_base_response import AppBaseResponse


class SignInResponse(AppBaseResponse):

    token: str

