from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LibUser, Book

# Register the custom user model with Django's built-in UserAdmin
admin.site.register(LibUser, UserAdmin)

# Optional: Register the Book model to manage books in the admin panel
admin.site.register(Book)
