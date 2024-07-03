from django.contrib import admin
from .models import User, Employee,Category_table,product,cart,cart_item

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Category_table)
admin.site.register(product)
admin.site.register(cart)
admin.site.register(cart_item)