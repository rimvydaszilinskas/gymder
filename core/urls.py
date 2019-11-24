"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include(('apps.api.urls', 'api'), namespace='api')),
    
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),
    url(r'^activities/', include(('apps.activities.urls', 'activities'), namespace='activities')),
    url(r'^m/', include(('apps.mobile.urls', 'mobile'), namespace='mobile')),
    url(r'', include(('apps.pages.urls', 'pages'), namespace='pages')),
    
]
