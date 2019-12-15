from datetime import datetime

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View

from apps.activities.models import Activity
from apps.activities.serializers import ActivitySerializer
from apps.pages.views_mixins import PageViewMixin

from .models import User
from .forms import AuthenticationForm
from .serializers import UserSerializer


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

        serializer = UserSerializer(user)

        activity_serializer = ActivitySerializer(
            activities, 
            many=True)

        return {
            'user': serializer.data,
            'owned_activities': activity_serializer.data
        }


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')

        return render(
            request,
            self.template_name)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password_repeat = request.POST.get('repeat_password', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        # terms = request.Post.get(bool="yes")

        try:
            if password != password_repeat:
                print('password do not match')
                return self.get(request, *args, **kwargs)

            user = User.objects.get(email=email)
            print('got email', email)
            print(user)
            return self.get(request, *args, **kwargs)
        except:
            user = User.objects.create_user(email, password)

            user.first_name = first_name
            user.last_name = last_name
            # user.terms = terms
            user.save()

            return redirect(reverse('users:login'))


class LoginView(View):
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        # check if user is already authenticated
        if request.user.is_authenticated:
            # check if it has next
            next_page = request.GET.get('next', None)

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
