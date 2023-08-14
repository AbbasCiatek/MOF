import re


def check_password_secure(password: str):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$'
    if not re.match(password_regex, password):
        return False
    return True
