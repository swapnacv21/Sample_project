from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Car_category(models.Model):
    name = models.TextField()
    image = models.FileField()

    def _str_(self):
        return self.name
    

class Cars(models.Model):
    car_id=models.TextField()
    car_name=models.TextField()
    car_year=models.IntegerField()
    car_place=models.TextField()
    car_rent=models.IntegerField()
    car_fuel=models.TextField()
    car_img=models.FileField()
    category=models.ForeignKey(Car_category,on_delete=models.CASCADE,related_name="cars")

# class Booking(models.Model):
#     car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name="bookings")
#     customer_name = models.CharField(max_length=255)
#     customer_email = models.EmailField()
#     customer_phone = models.CharField(max_length=15)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Confirmed", "Confirmed")], default="Pending")

#     def _str_(self):
#         return f"Booking for {self.car.car_name} by {self.customer_name}"
    