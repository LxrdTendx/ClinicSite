from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'country_of_origin', 'discount_percent']
    list_filter = ['type', 'country_of_origin']
    search_fields = ['name']
