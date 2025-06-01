import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from const.const import USERNAME_VALIDATION_MESSAGE


@deconstructible
class AllowedCharactersUsernameValidator:
    def __init__(self, pattern=r"^[\w.@+-]+$"):
        self.pattern = pattern
        self.regex = re.compile(pattern)

    def __call__(self, value):
        if not self.regex.fullmatch(value):
            raise ValidationError(USERNAME_VALIDATION_MESSAGE)

    def get_help_text(self):
        return (USERNAME_VALIDATION_MESSAGE)
