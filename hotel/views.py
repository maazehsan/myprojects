from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message

def page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        # Create user only in POST request
        user = User.objects.create_user(username=username, email=email)
        Message.objects.create(user=user, subject=subject, message=message)
        
        # Redirect after successful form submission
        return redirect('page')
    
    # Only render template for GET requests
    return render(request, 'hotel/index.html')