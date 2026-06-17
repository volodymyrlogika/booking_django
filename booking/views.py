from django.shortcuts import render
from django.contrib import messages
import booking
from .models import Apartment, Booking

def home(request):

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    apartments = Apartment.objects.all()

    if check_in and check_out:
        apartments = apartments.exclude(
            bookings__check_in__lt=check_out,
            bookings__check_out__gt=check_in
        )   

    return render(request, 'home.html', {'apartments': apartments, 'check_in': check_in, 'check_out': check_out})


def apartment_page(request, apartment_id):
    apartment = Apartment.objects.get(id = apartment_id)
    return render(request, 'apartment_page.html', {'apartment': apartment})


def booking_page(request, apartment_id):
    apartment = Apartment.objects.get(id = apartment_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Тут має бути валідація даних та обробка помилок
        existing_bookings = Booking.objects.filter(
            apartment=apartment,
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        if existing_bookings.exists():
            messages.error(request, 'Ці дати вже заброньовані. Будь ласка, виберіть інші дати.')
        else:
            booking = Booking.objects.create(
                apartment=apartment,
                check_in=check_in,
                check_out=check_out,
                name=name,
                surname=surname,
                email=email,
                phone=phone,
                total_price=apartment.price,  # Тут можна додати логіку для обчислення ціни
                user = request.user if request.user.is_authenticated else None
            )
            return render(request, 'booking_confirmed.html', {'apartment': apartment, 'booking': booking})
    
    return render(request, 'booking.html', {'apartment': apartment })