from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm)

User = get_user_model()

class AuthenticationForm(DjangoAuthenticationForm):
    def clean(self):
        username = self.cleaned_data('username', None)
        password = self.cleaned_data('password', None)

        if username is not None and password:
            username = username.lower()

            self.user_cache = authenticate(
                request=self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name})
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
