from functools import wraps

from flask import Response, session


def unauthorized_if_no_session_cookie(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        # If there is no session cookie, return a 401: Unauthorized response.
        if "athlete_id" not in session:
            return Response(response="Unauthorized", status=401)

        # If the session cookie is present, proceed with the original view function
        return view_func(*args, **kwargs)

    return decorated_view
