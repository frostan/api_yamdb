from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'bio',
        'role',
    )
    list_editable = ('role',)
    empty_value_display = '-пусто-'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация',
         {'fields': ('first_name', 'last_name', 'bio', 'email')}
         )
    )
