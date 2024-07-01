from django.contrib import admin
from .models import User, Employee,Category_table,product

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Category_table)
admin.site.register(product)