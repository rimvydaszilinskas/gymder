from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password,  **kwargs):
        if not email:
            raise ValueError(_('Email must be provided'))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have staff status set to true'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have staff status set to true'))
    
        self.create_user(email, password, **kwargs)
