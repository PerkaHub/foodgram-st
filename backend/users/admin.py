from django.contrib import admin

from .models import User
from const.const import SEARCH_EMAIL_USERNAME

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "password"
    )
    search_fields = ("email", "username")
    search_help_text = SEARCH_EMAIL_USERNAME
