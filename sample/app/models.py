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