from django.db import models
from django.contrib.auth.models import AbstractUser

class LibUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('borrower', 'Borrower')
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='borrower')

    class Meta:
        verbose_name = 'Library User'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='libuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='libuser_permissions',
        blank=True,
    )

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    quantity = models.IntegerField()
    borrowed = models.IntegerField()

class BorrowRecord(models.Model):
    user = models.ForeignKey(LibUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)  # blank if not returned yet
