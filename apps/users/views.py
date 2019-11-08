from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View


from .models import User


class ProfileView(View):
    template_name = 'users/profile.html'

    def create_js_context(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        self.override_title('{} Profile'.format(user.display_name))


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse('users:login') + '?next={}&require=true'.format(reverse('users:profile')))

        return super().get(request, *args, **kwargs)


class RegisterView(View):
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
        terms = request.Post.get(bool="yes")

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
            user.terms = terms
            user.save()

            return redirect(reverse('users:login'))


class LoginView(View):
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

