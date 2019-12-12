from django.db import models


class BaseManager(models.Manager):
    def only_active(self):
        return self.exclude(is_deleted=True)
