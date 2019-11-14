from django.contrib import admin

from .models import (
    ActivityType,
    GroupActivity,
    IndividualActivity,
    Request)


class ActivityTypeAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid',
        'approved',
        'is_deleted',
    ]

    list_filter = [
        'is_deleted',
        'approved'
    ]

    search_fields = [
        'uuid',
        'title'
    ]


class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid',
        'public',
        'time'
    ]

    raw_id_fields = [
        'address',
        'group',
        'activity_type',
        'user'
    ]


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid',
        'status',
        'is_deleted'
    ]

    raw_id_fields = [
        'activity',
        'user'
    ]


admin.site.register(ActivityType, ActivityTypeAdmin)
admin.site.register(IndividualActivity, ActivityAdmin)
admin.site.register(GroupActivity, ActivityAdmin)
admin.site.register(Request, RequestAdmin)
