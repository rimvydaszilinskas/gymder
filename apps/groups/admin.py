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

    raw_id_fields = [
        'user'
    ]


class MembershipAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]

    raw_id_fields = [
        'user',
        'group'
    ]


admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, MembershipAdmin)
