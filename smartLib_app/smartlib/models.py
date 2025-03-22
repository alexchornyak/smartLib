from django.db import models
from django.contrib.auth.models import AbstractUser
# Database structure

class LibUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('borrower', 'Borrower')
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='borrower')

    class Meta:
        # Optionally specify the model's default permissions or any other custom settings
        verbose_name = 'Library User'

    # You can add related_name to avoid the conflict
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='libuser_set',  # Custom related name to resolve conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='libuser_permissions',  # Custom related name to resolve conflict
        blank=True,
    )
    
    class Book(models.Model):
        title = models.CharField(max_length=100)
        author = models.CharField(max_length=100)
        genre = models.CharField(max_length=100)
        quantity = models.IntegerField()
        borrowed = models.IntegerField()

  
