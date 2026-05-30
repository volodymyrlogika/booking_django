from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    TYPE_ROOM_CHOICES = [
        ('single', 'Одиночний номер'),
        ('double', 'Двомісний номер'),  
        ('suite', 'Люкс'),
        ('family', 'Сімейний номер'),
        ('studio', 'Студія'),
        ('penthouse', 'Пентхаус'),        
    ]

    title = models.CharField(max_length=100, verbose_name="Назва апартаментів")
    location = models.CharField(max_length=255, verbose_name="Розташування")
    image = models.ImageField(upload_to='apartment_images/', null=True, blank=True, verbose_name="Зображення")
    description = models.TextField(null=True, blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10,  decimal_places=2, verbose_name="Ціна")
    capacity = models.IntegerField(default=1, verbose_name="Місткість")

    type_room = models.CharField(max_length=50, choices=TYPE_ROOM_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.location} - ${self.price} грн"

    class Meta:
        verbose_name = "Апартаменти"
        verbose_name_plural = "Апартаменти"
        ordering = ['title','price' ]


class Booking(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name="Апартаменти")
    check_in = models.DateTimeField(verbose_name="Дата заїзду")
    check_out = models.DateTimeField(verbose_name="Дата виїзду")

    name = models.CharField(max_length=50, verbose_name="Ім'я")
    surname = models.CharField(max_length=50, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="Електронна пошта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Загальна ціна")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Користувач")

    def __str__(self):
        return f"Бронювання: {self.apartment.title} - {self.name} {self.surname} - {self.check_in.date()} до {self.check_out.date()} - ${self.total_price} грн"
    
    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"
        ordering = ['-created_at']

