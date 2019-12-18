import re

from django.conf import settings
from django.shortcuts import redirect, reverse


EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Helps with redirecting based on user authentication status

    Check `settings/base.py` file for url definitions
    `LOGIN_URL` and `LOGIN_EXEMPT_URLS` are urls available for the users that are not authenticated
    `LOGIN_REDIRECT_URL` is for authenticated users if they try to access public routes
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # check if request is not broken
        assert hasattr(request, 'user')

        path = request.path_info.lstrip('/')

        # If user is not authenticated and trying to access login required data, redirect to login
        if not request.user.is_authenticated:
            if not any(url.match(path) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)

        # Booleans
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        url_is_global = any(url.match(path) for url in [re.compile(_) for _ in settings.ALLOW_ALL_URLS])
        
        # If user wants to logout, always allow
        if path == reverse('users:logout').lstrip('/'):
            return None
        elif url_is_global:
            # if url is global, do nothing and continue with request
            return None
        elif request.user.is_authenticated and url_is_exempt:
            # If user is authenticated and trying to access data for not authenticated users, send him to his profile
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt:
            # Let it be
            return None
