from functools import wraps
from flask import request, current_app as app


def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') == 'S5Umpe7q0OXp9SE6mAg36Eu5Zmq27XF9XH0KA5p2':
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function