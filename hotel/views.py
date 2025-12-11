from django.shortcuts import render, redirect

def page(request):
    return render(request, 'hotel/index.html')