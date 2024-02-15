import re
from typing import Any

from django.core.exceptions import ValidationError


def validate_password_digit(value: str) -> Any:
    if not re.search(r"[\d]+", value):
        raise ValidationError("The password must contain at least one digit")
    else:
        return value


def validate_password_uppercase(value: str) -> Any:
    if not re.search(r"[A-Z]+", value):
        raise ValidationError(
            "The password must contain at least one uppercase character"
        )
    else:
        return value


def validate_password_symbol(value: str) -> Any:
    if not re.search(r"[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]+", value):
        raise ValidationError(
            "The Password must contain at least one special characters"
        )
    else:
        return value


def validate_password_lowercase(value: str) -> Any:
    if not re.search(r"[a-z]+", value):
        raise ValidationError(
            "The password must contain at least one lowercase character"
        )
    else:
        return value
