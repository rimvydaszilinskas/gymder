from django.contrib import admin

from .models import Group, Membership


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]


admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, GroupAdmin)
