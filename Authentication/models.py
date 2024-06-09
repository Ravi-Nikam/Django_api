from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser
from Authentication.manager import UserManager

# Create your models here.

class Gender_option(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'X', 'Other'


class User(AbstractBaseUser):
    print("3***************************")
    username = None
    phone_number  = models.IntegerField(null=True)
    email = models.EmailField(unique=True)
    dob = models.CharField(max_length=10)
    Gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female'),('X', 'Other')])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'  # MEANS PHONE NUMBER IS WORK AS A username
    REQUIRED_FIELDS = ['first_name','last_name','Gender','phone_number',"dob"]
    # REQUIRED_FIELDS = []
    
    print("4***************************")

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Employee(models.Model):
    First_Name  = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.TextField()
    Phone_Number = models.IntegerField()
    Gender = models.CharField(max_length=1,choices=Gender_option.choices)
    
    def __str__(self):
        return self.Email
    
    
    