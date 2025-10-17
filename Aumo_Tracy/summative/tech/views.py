from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # make sure you have a User model in models.py

def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')

        try:
            # get user by email or phone
            if '@' in email_or_phone:
                user = User.objects.get(email=email_or_phone, password=password)
            else:
                user = User.objects.get(phone=email_or_phone, password=password)

            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('success')  # redirect to success page
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # check if user exists
        if User.objects.filter(email=email).exists() or User.objects.filter(phone=phone).exists():
            messages.error(request, "User with this email or phone already exists.")
            return render(request, 'signup.html')

        # create user
        user = User.objects.create(name=name, email=email, phone=phone, password=password)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')


def success_view(request):
    return render(request, 'success.html')
