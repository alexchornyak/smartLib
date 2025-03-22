from django import forms
from django.core.validators import EmailValidator

# For forms (signup/login/etc.)+
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(validators=[EmailValidator()], label='Your Email')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')