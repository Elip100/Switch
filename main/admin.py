from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class NewUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ("Extra", {"fields": ["account_type"]})
    )

admin.site.register(User, NewUserAdmin)