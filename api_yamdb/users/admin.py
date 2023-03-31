from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'date_joined')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
