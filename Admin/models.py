from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class Gender_option(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'X', 'Other'


class CustomUser(AbstractUser):
    username = None
    phone_number  = models.IntegerField(default="000")
    email = models.EmailField(unique=True)
    Gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female'),('X', 'Other')], default='M')
    
    USERNAME_FIELD = 'email'  # MEANS PHONE NUMBER IS WORK AS A username
    REQUIRED_FIELDS = ['first_name','last_name','Gender','phone_number']
    
    objects = UserManager()

class Employee(models.Model):
    First_Name  = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.TextField()
    Phone_Number = models.IntegerField()
    Gender = models.CharField(max_length=1,choices=Gender_option.choices)
    
    def __str__(self):
        return self.Email
    
    
    