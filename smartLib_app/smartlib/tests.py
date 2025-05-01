
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import Book, BorrowRecord
import json

User = get_user_model()

class SmartLibTestCase(TestCase):
    """Basic functionality tests: signup, login, borrowing, returning, contact form."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            genre="Fiction",
            quantity=5,
            borrowed=0,
            thumbnail="http://example.com/thumb.jpg",
            preview_link="http://books.google.com/preview?id=abc123",
            google_book_id="abc123"
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_signup_and_login(self):
        # Signup
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)

        # Login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_logout(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_dashboard_access(self):
        response = self.client.get(reverse('dash'))
        self.assertRedirects(response, f"/login/?next=/dash/")

        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('dash'))
        self.assertEqual(response.status_code, 200)

    def test_borrow_and_return_book(self):
        self.client.login(username='testuser', password='pass123')

        # Borrow
        self.client.get(reverse('borrow_book', args=[self.book.id]))
        self.book.refresh_from_db()
        self.assertEqual(self.book.borrowed, 1)
        self.assertEqual(BorrowRecord.objects.count(), 1)

        # Return
        record = BorrowRecord.objects.get(user=self.user, book=self.book)
        self.client.get(reverse('return_book', args=[record.id]))
        record.refresh_from_db()
        self.assertIsNotNone(record.return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.borrowed, 0)

    def test_read_book_view(self):
        self.client.login(username='testuser', password='pass123')
        self.client.get(reverse('borrow_book', args=[self.book.id]))
        record = BorrowRecord.objects.get(user=self.user, book=self.book)
        response = self.client.get(reverse('read_book', args=[record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('google_book_id', response.context)

    def test_borrowed_titles_endpoint(self):
        self.client.login(username='testuser', password='pass123')
        self.client.get(reverse('borrow_book', args=[self.book.id]))
        response = self.client.get(reverse('borrowed_titles'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.book.title, response.json().get('titles', []))

    def test_checkout_book_api(self):
        self.client.login(username='testuser', password='pass123')
        payload = {
            'title': 'New Book',
            'author': 'API Author',
            'genre': 'Unknown',
            'quantity': 1,
            'thumbnail': 'http://example.com/image.png',
            'preview_link': 'http://preview.link',
            'book_id': 'api123'
        }
        response = self.client.post(
            reverse('checkout_book'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')

    def test_contact_form_html(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Jane',
            'email': 'jane@example.com',
            'subject': 'Support',
            'message': 'Need assistance.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane')

    def test_contact_form_json(self):
        payload = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Help',
            'message': 'This is a test message.'
        }
        response = self.client.post(
            reverse('contact'),
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')
