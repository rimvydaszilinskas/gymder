from django.contrib import admin

from .models import Tag, Address


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]

admin.site.register(Address, AddressAdmin)
admin.site.register(Tag, AddressAdmin)