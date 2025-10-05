import os
import json

from .models import LoginAttempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

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

@csrf_exempt
def submit_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Incorrect HTTP method used'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'success': False, 'error': 'Missing email or password'}, status=400)
        
        # Try to authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # logs user into Django session
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful"})
        else:
            return JsonResponse({"success": False, "error": "Invalid credentials"}, status=401)
                
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
'''

def home(request):
    # Path to the static index.html
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    index_path = os.path.join(base_dir, 'frontend', 'index.html')
    try:
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    except FileNotFoundError:
        raise Http404('index.html not found')
    
@csrf_exempt
def submit_signup(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid HTTP request made'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'success': False, 'error': 'Mising email or password'}, status=400)
        
        # 🔎 Check if email already exists
        if LoginAttempt.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'User already exists'}, status=400)
        
        # Save into my PostgreSQL LoginAttempt table
        attempt = LoginAttempt.objects.create(
            email=email,
            password=make_password(password) # 🔒 hash the password
        )
        
        return JsonResponse({'success': True, 'message': 'Signup successful', 'id': attempt.id}, status=200)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)