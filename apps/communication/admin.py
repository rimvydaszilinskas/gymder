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


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'uuid'
    ]

    list_fields = [
        '__str__',
        'uuid'
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)