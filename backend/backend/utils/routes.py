from fastapi import Request
from fastapi.exceptions import HTTPException


# Dependency to check for a cookie
def unauthorized_if_no_session_token(request: Request):
    # Check for the "session_token" in cookies
    if "session_token" not in request.cookies:
        raise HTTPException(status_code=401, detail="Unauthorized")
