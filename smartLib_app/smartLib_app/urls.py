from django.contrib import admin
from smartlib import views
from django.urls import path
from smartlib.views import (
    index,
    login_view,
    logout_view,
    signup_view,
    contact,
    success,
    dash,
    borrow_book,
    return_book,
    checkout_book,  # 👈 New view added!
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
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:record_id>/', return_book, name='return_book'),
    path('checkout/', checkout_book, name='checkout_book'),
    path('borrowed_titles/', views.borrowed_titles, name='borrowed_titles'),
    path('read_book/<str:record_id>/', views.read_book, name='read_book'),
]
