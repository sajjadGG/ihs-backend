"""ihs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#TODO : module from other app should not be here
from django.contrib import admin
from django.urls import path , include 
from rest_framework.authtoken.views import obtain_auth_token
from core.urls import router

from django.conf import settings
from django.conf.urls.static import static
from core.views import CustomObtainAuthToken

#path(r'api/token/' , include('rest_framework.urls') , name='api-token')

urlpatterns = [
    path(r'api/token/' , CustomObtainAuthToken.as_view() , name='api-token'),
    path(r'api/login/', include('rest_framework.urls')),
    path(r'api/' , include(router.urls)),
    path(r'chat/', include('chat.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
