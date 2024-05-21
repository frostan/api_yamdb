from django.contrib import admin

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'bio',
        'confirmation_code',
        'role',
    )
    list_editable = ('role',)
    empty_value_display = 'пусто'


admin.site.register(CustomUser, UserAdmin)
