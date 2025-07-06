import os
import requests
import jwt


def test_sign_in():
    URL_2 = "http://127.0.0.1:12345"
    URL = "http://host.docker.internal:12345/api/v1/user/login"
    creds = {"email": os.getenv("EMAIL"), "password": os.getenv("PASSWORD")}
    sign_in_request = requests.post(url=URL, json=creds)
    assert sign_in_request.status_code == 200
    assert sign_in_request.json().get("message") == "User signed in successfully"
    assert sign_in_request.json().get("user_id") == 2


def test_token():
    URL_2 = "http://127.0.0.1:12345"
    URL = "http://host.docker.internal:12345/api/v1/user/login"
    creds = {"email": os.getenv("EMAIL"), "password": os.getenv("PASSWORD")}
    sign_in_request = requests.post(url=URL, json=creds)
    assert sign_in_request.status_code == 200

    token = sign_in_request.json().get("token")
    decoded = jwt.decode(token, key=os.getenv("SECRET"), algorithms="HS256")
    assert decoded.get('email') == os.getenv("EMAIL")
    assert decoded.get('user_id') == 2