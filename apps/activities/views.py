from django.views import View
from django.shortcuts import render

from apps.pages.views_mixins import PageViewMixin
from apps.users.serializers import UserSerializer


class CreateActivityView(PageViewMixin):
    BUNDLE_NAME = 'create_activity'

    def create_js_context(self, request, *args, **kwargs):
        # Return user data as JSON to the JS view
        user = request.user

        serializer = UserSerializer(user)

        return {'user': serializer.data}
