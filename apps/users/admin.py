from django.contrib import admin

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid',
        'password'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]

    raw_id_fields = [
        'address'
    ]


class ApiToken(Token):
    """ Proxy the token model to display it under users """
    class Meta:
        proxy = True


admin.site.register(User, UserAdmin)
admin.site.register(ApiToken, TokenAdmin)
admin.site.unregister(Token)
