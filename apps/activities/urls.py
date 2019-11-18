from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^create/$', views.CreateActivityView.as_view(), name='create-activity'),
    
]
