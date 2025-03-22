from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Most backend processing and rendering html/php files

def login_view(request):
    return render(request, 'profile.html')

# For contact form
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send the email
            send_mail(
                subject,
                message,
                email,
                [settings.CONTACT_EMAIL],
                fail_silently=False
            )

            # After sending the email, a success page is shown
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def success(request):
    name = request.GET.get('name', 'Guest')  # Default to 'Guest' if no name is passed
    return render(request, 'success.html', {'name': name})


