from marshmallow import ValidationError
from functools import wraps
from flask import jsonify


def error_handler(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return jsonify(e.messages), 400
    return wrapped
