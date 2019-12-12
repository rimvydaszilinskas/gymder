from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Group, Membership


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid',
        'link_to_group',
    ]

    list_display = [
        '__str__',
        'uuid',
    ]

    raw_id_fields = [
        'user'
    ]

    @mark_safe
    def link_to_group(self, obj):
        if obj is not None and obj.uuid:
            return '<a href="{0}">{1}</a>'.format(reverse('groups:preview', args=[obj.uuid.hex]), obj.title)
        return '-'

    link_to_group.short_description = 'Link to preview'
    link_to_group.allow_tags = True


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
