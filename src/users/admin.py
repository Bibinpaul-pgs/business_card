from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# local
from .models import User


admin.site.register(User)
# class UserAdmin(BaseUserAdmin):
#     """ user admin """
