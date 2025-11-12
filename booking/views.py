from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    return render(request, 'booking/index.html')

def book_appointment(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone')
            
            # Create username from first and last name
            username = f"{first_name.lower()}{last_name.lower()}"
            
            # Check if user with this email already exists
            existing_user = User.objects.filter(email=email).first()
            
            if existing_user:
                user = existing_user
            else:
                # Make username unique if it already exists
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
            
            # Create booking
            booking = Booking.objects.create(
                user=user,
                phone_number=phone_number
            )
            
            messages.success(request, 'Appointment request submitted successfully!')
            return render(request, 'booking/booking.html', {'success': True})
            
        except Exception as e:
            messages.error(request, f'Error submitting appointment: {str(e)}')
            return render(request, 'booking/booking.html', {'error': str(e)})
    
    return render(request, 'booking/booking.html')