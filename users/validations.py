import re

from .exceptions import PasswordValidationError

def validate_password(password):
    if not re.compile(
        "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
        ).match(password):
        raise PasswordValidationError

    return