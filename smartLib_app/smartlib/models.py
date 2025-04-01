from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model
class LibUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('borrower', 'Borrower'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='borrower')

# Book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)  # Ensure positive numbers

    def available_copies(self):
        borrowed_count = Borrow.objects.filter(book=self, returned=False).count()
        return self.quantity - borrowed_count

    def __str__(self):
        return f"{self.title} by {self.author}"

# Borrow model to track borrowed books
class Borrow(models.Model):
    user = models.ForeignKey(LibUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
