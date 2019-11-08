from django.shortcuts import render, redirect
from django.views import View


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/register.html', {})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            # TODO redirect somewhere good!
            return redirect('pages:index')
        return render(request, 'users/login.html', {})
