from django.shortcuts import render
from .models import Apartment, Booking

def home(request):
    apartments = Apartment.objects.all()
    return render(request, 'home.html', {'apartments': apartments})

