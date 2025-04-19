from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.http import JsonResponse
import json

# Most backend processing and rendering html/php files

def index(request):
    return render(request, 'index.html')

def dash(request):
    return render(request, 'dash.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

# For contact form
def contact(request):
    if request.method == 'POST':
        # JSON submission from JS (AJAX)
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

        # Fallback: regular HTML form submission
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

def success(request):
    name = request.GET.get('name', 'Guest')  # Default to 'Guest' if no name is passed
    return render(request, 'success.html', {'name': name})




