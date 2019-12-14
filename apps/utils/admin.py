from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Tag, Address


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]

    raw_id_fields = [
        'user'
    ]


class TagAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]


admin.site.register(Address, AddressAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(Group)
