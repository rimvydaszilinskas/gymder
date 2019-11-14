from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_fields = [
        '__str__',
        'uuid'
    ]

    raw_id_fields = [
        'user',
        'group',
        'activity'
    ]


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_fields = [
        '__str__',
        'uuid'
    ]

    raw_id_fields = [
        'user',
        'post'
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)