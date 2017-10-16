from flask import request, Response
from functools import wraps

import Response


def login(username, password):
    return username == 'admin' and password == 'admin'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not login(auth.username, auth.password):
            return Response.unauthorised()
        return f(*args, **kwargs)
    return decorated
