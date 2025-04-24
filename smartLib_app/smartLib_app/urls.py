from django.contrib import admin
from django.urls import path
from smartlib.views import (
    contact,
    success,
    index,
    dash,
    login_view,
    signup_view,
    logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('dash/', dash, name='dash'),
]
