from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser
from Authentication.manager import UserManager
from django.utils.crypto import get_random_string
from django.utils.text import slugify


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
    gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female'),('X', 'Other')])
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
    REQUIRED_FIELDS = ['first_name','last_name','gender','phone_number',"dob"]
    # REQUIRED_FIELDS = []
    
    print("4***************************")

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def print_user_model_fields():
        user = User()
        for field in user._meta.get_fields():
            print(field.name)

        print_user_model_fields()


class Employee(models.Model):
    First_Name  = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.TextField()
    Phone_Number = models.IntegerField()
    Gender = models.CharField(max_length=1,choices=Gender_option.choices)
    
    def __str__(self):
        return self.Email
    

    
from django.db import models
from django.urls import reverse


# Create your models here.
# create category table into database.

class Category_table(models.Model):
    cname = models.CharField(max_length=200, primary_key=True)
    slug = models.SlugField(max_length=200, unique=True, default='')  # slug is a unique for category.
    cat_img = models.ImageField(upload_to="category_list", default="default.png")
    category_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cname

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


def images_upl(instance, filename):
    return 'cat_rel_product/{0}/{1}'.format(instance.category.cname, filename)


def custom_slug(name,artist):
    custom_string = name + str(artist) + " " + get_random_string(length=8) 
    
    slug = slugify(custom_string)

    while product.objects.filter(slug=slug).exists():
        slug = slugify(custom_string) + get_random_string(length=4)

    return slug


class product(models.Model):
    category = models.ForeignKey(Category_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    image = models.ImageField(upload_to=images_upl, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    brand = models.CharField(max_length=10)
    size = models.CharField(max_length=3,default="None")
    available = models.BooleanField(default=True)
    dates=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + "****" + self.slug

    def get_absolute_url(self):
        return reverse("cat_rel_pro", kwargs={"slug": self.slug})
    
    
    def save(self,*args,**kwargs):
        # modify_lyr_name(self.Song_Lyrics_File.path) # calling converting file function
        self.slug = custom_slug(self.name,self.brand)
        super().save(*args,**kwargs)
        

# whole cart
class cart(models.Model):
    user_cart_item = models.ForeignKey(User, on_delete=models.CASCADE) # which users cart
    created = models.DateTimeField(auto_now_add=True)
    
    
    # def total_price():
    #     total = 0
    #     for item in cart_item.objects.all():
    #         total += item.cart_total_item
    #     return total
            
            
class cart_item(models.Model): # cart details item
    cart_id = models.ForeignKey(cart,on_delete=models.CASCADE,default=1)
    cart_item_id = models.AutoField(primary_key=True)
    product_cart_item  = models.ForeignKey(product, on_delete=models.CASCADE) # Product in card
    cart_quantity_item = models.PositiveIntegerField(default=1) # total item
    cart_total_item = models.IntegerField() # cart amount 
    
    
    # def total_cart_amount():
    #     total = 0
    #     for item in cart_item.objects.all():
    #         total += item.cart_total_item
    #     return total