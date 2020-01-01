from datetime import datetime

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View

from apps.activities.models import Activity
from apps.activities.serializers import ActivitySerializer
from apps.pages.views_mixins import PageViewMixin

from apps.utils.serializers import TagSerializer

from .models import User
from .forms import AuthenticationForm
from .serializers import UserSerializer, DetailedUserSerializer


class SelfProfileView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('users:user-profile', args=[request.user.uuid.hex]))


class ProfileView(PageViewMixin):
    BUNDLE_NAME = 'profile'

    def create_js_context(self, request, *args, **kwargs):
        user = get_object_or_404(User, uuid=kwargs['uuid'], is_deleted=False)
        self.TITLE = '{} Profile'.format(user.username if user.username else user.email)
        activities = Activity.objects.only_active().filter(
            user=user,
            public=True,
            time__gte=datetime.today())

        serializer = DetailedUserSerializer(user)

        activity_serializer = ActivitySerializer(
            activities, 
            many=True)

        return {
            'user': serializer.data,
            'owned_activities': activity_serializer.data
        }


class ProfileSettingsView(PageViewMixin):
    BUNDLE_NAME = 'profile_settings'
    TITLE = 'Settings'

    def create_js_context(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)

        tags_serializer = TagSerializer(request.user.tags.all(), many=True)

        return {
            'user': serializer.data,
            'tags': tags_serializer.data
        }


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')

        context = {}

        if 'registration_errors' in kwargs:
            context['error'] = kwargs['registration_errors']

        return render(
            request,self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password_repeat = request.POST.get('password_repeat', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)

        # Check if the data exists in the request
        if email is None or password is None \
            or password_repeat is None \
                or first_name is None or last_name is None:
            kwargs['registration_errors'] = 'Please fill all the fields'
            return self.get(request, *args, **kwargs)

        try:
            if password != password_repeat:
                kwargs['registration_errors'] = 'Passwords do not match'
                return self.get(request, *args, **kwargs)

            user = User.objects.get(email=email)

            kwargs['registration_errors'] = 'Email is already registered'
            return self.get(request, *args, **kwargs)
        except:
            user = User.objects.create_user(
                email, 
                password, 
                first_name=first_name, 
                last_name=last_name)

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect(reverse('users:login') + '?registered=True&email={}'.format(email))


class LoginView(View):
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        # check if user is already authenticated
        if request.user.is_authenticated:
            # check if it has next
            next_page = request.GET.get('next', None)
            registered_email = request.GET.get('email', None)

            if registered_email:
                kwargs['email'] = registered_email

            if next_page:
                return redirect(next_page)
            return redirect(reverse('users:profile'))

        return render(
            request,
            'users/login.html')

    def post(self, request, *args, **kwargs):

        form = self.form_class(request, data=request.POST)

        if form.is_valid:
            email = request.POST['email'].lower()
            password = request.POST['password']

            user = authenticate(request=request, email=email, password=password)

            if user is not None:
                login(request, user)

            return self.get(request, *args, **kwargs)


class LogoutView(View):
    """ Logout user and redirect to login page """

    def get(self, request,  *args, **kwargs):
        logout(request)
        return redirect(reverse('users:login'))
