from django.db import models

from apps.utils.models import BaseModel


class Post(BaseModel):
    body = models.TextField(
        null=False,
        blank=False)
    
    user = models.ForeignKey(
        'users.User',
        related_name='posts',
        on_delete=models.CASCADE)

    group = models.ForeignKey(
        'groups.Group',
        null=True,
        blank=True,
        related_name='posts',
        on_delete=models.CASCADE)

    activity = models.ForeignKey(
        'activities.Activity',
        null=True,
        blank=True,
        related_name='posts',
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Comment(BaseModel):
    body = models.TextField(
        blank=True,
        null=True)

    user = models.ForeignKey(
        'users.User',
        related_name='comments',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
