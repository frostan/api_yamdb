from django.contrib import admin

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'confirmation_code',
        'user_role',
    )
    list_editable = ('user_role',)
    empty_value_display = 'пусто'


admin.site.register(CustomUser, UserAdmin)
