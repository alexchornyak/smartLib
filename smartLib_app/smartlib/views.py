from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ContactForm, SignupForm
from .models import LibUser
from django.http import JsonResponse
import json

# Homepage
def index(request):
    return render(request, 'index.html')

# Dashboard page
def dash(request):
    return render(request, 'dash.html')

# Signup view
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

# Login view
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

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Contact view (with AJAX + fallback)
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

        # HTML form fallback
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
