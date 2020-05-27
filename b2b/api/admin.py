from django.contrib import admin
from .models import Company, Order, Product, OrderPosition
# Register your models here.

admin.site.register(Company)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderPosition)
