from django.db import models
from django.contrib.auth.models import AbstractUser
# Database structure

class LibUser(AbstractUser):
    USER_ROLES = (
        {'admin', 'Admin'},
        {'borrower', 'Borrower'}
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='borrower')

    class Book(models.Model):
        title = models.CharField(max_length=100)
        author = models.CharField(max_length=100)
        genre = models.CharField(max_length=100)
        quantity = models.IntegerField()
        borrowed = models.IntegerField()

  
