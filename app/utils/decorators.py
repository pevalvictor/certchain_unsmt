from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator
