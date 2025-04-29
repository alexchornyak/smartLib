from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .forms import ContactForm, SignupForm
from .models import LibUser, Book, BorrowRecord
import json



# Homepage
def index(request):
    return render(request, 'index.html')

# Dashboard - Show user's borrowed books and available books
@login_required(login_url="/login/")
def dash(request):
    my_borrows = BorrowRecord.objects.filter(user=request.user, return_date__isnull=True)
    return render(request, 'dash.html', {
        'my_borrows': my_borrows,
    })

# Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url="/login/")
def borrowed_titles(request):
    borrowed = BorrowRecord.objects.filter(user=request.user, return_date__isnull=True)
    titles = [record.book.title for record in borrowed]
    return JsonResponse({'titles': titles})


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Borrow book
@login_required(login_url="/login/")
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.quantity > book.borrowed:
        book.borrowed += 1
        book.save()
        BorrowRecord.objects.create(user=request.user, book=book)
    return redirect('dash')

# Return book
@login_required(login_url="/login/")
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, pk=record_id)
    if record.user == request.user and record.return_date is None:
        record.return_date = now()
        record.book.borrowed -= 1
        record.book.save()
        record.save()
    return redirect('dash')

# Contact form
def contact(request):
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                name = data.get('name')
                email = data.get('email')
                subject = data.get('subject')
                message = data.get('message')

                send_mail(
                    subject,
                    message,
                    email,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False
                )
                return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject,
                message,
                email,
                [settings.CONTACT_EMAIL],
                fail_silently=False
            )
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Success page
def success(request):
    name = request.GET.get('name', 'Guest')
    return render(request, 'success.html', {'name': name})

# Checkout new book from API (homepage)
@csrf_exempt
@login_required(login_url="/login/")
def checkout_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre', 'Unknown')
        quantity = data.get('quantity', 1)

        book, created = Book.objects.get_or_create(
            title=title,
            author=author,
            defaults={'genre': genre, 'quantity': quantity, 'borrowed': 1}
        )

        if not created:
            if book.quantity > book.borrowed:
                book.borrowed += 1
                book.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'No more copies available.'})

        BorrowRecord.objects.create(user=request.user, book=book)

        return JsonResponse({'status': 'success', 'message': 'Book checked out successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
