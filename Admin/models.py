from django.db import models

# Create your models here.


class Gender_option(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'X', 'Other'
    
class Employee(models.Model):
    First_Name  = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.TextField()
    Phone_Number = models.IntegerField()
    Gender = models.CharField(max_length=1,choices=Gender_option.choices)
    
    def __str__(self):
        return self.Email
    
    
    