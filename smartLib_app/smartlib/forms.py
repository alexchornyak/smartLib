from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from .models import LibUser

# Contact form
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(validators=[EmailValidator()], label='Your Email')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')

# Signup form using custom LibUser model
class SignupForm(UserCreationForm):
    class Meta:
        model = LibUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
