from django.contrib import admin

from .models import (
    Activity,
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
        'uuid'
    ]


class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_display = [
        '__str__',
        'uuid'
    ]


admin.site.register(ActivityType, ActivityTypeAdmin)
admin.site.register(IndividualActivity, ActivityAdmin)
admin.site.register(GroupActivity, ActivityAdmin)
admin.site.register(Request, RequestAdmin)
