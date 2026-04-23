from fastapi import Response

AUTH_COOKIE_NAME = "example_access_token"

def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax"
    )

def remove_auth_cookie(response: Response):
    response.delete_cookie(key="AUTH_COOKIE_NAME", path="/")