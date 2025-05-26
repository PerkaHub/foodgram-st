import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            _("Имя пользователя 'me' не разрешено.")
        )
    if not re.match(r"^[\w.@+-]+$", value):
        raise ValidationError(
            _("Имя может содержать только буквы, цифры и знаки @/./+/-/_")
        )
    return value
