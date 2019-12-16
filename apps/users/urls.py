from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^profile/$', views.SelfProfileView.as_view(), name='profile'),
    url(r'^profile/settings/$', views.ProfileSettingsView.as_view(), name='profile-settings'),
    url(r'^profile/(?P<uuid>\w+)/', views.ProfileView.as_view(), name='user-profile'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
