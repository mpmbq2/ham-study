import os


def get_username() -> str:
    username = os.environ.get("HTTP_X_RSTUDIO_CONNECT_USER_NAME")
    if username:
        return username.lower()
    return "local"
