from django.shortcuts import render, redirect
def index(request):
    return render(request, 'booking/index.html')

def book_appointment(request):
    return render(request, 'booking/booking.html')