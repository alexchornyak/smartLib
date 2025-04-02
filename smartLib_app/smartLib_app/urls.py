"""
URL configuration for smartLib_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from smartlib import views
from smartlib.views import contact, success, index, dash, login, signup

# Define paths to pages within the app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('dash/', dash, name='dash'),
    path('signup/', signup, name='signup'),

]
