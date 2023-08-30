from django.contrib import admin

# Register your models here.
from .models import Product, Category, Genre, Platform

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Platform)