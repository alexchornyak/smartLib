from django.shortcuts import render

# Most backend processing and rendering html/php files

def login_view(request):
    return render(request, 'profile.html')

