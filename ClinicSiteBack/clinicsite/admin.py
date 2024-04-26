from django.contrib import admin

from .models import Product, Scientific, Certificates, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'tag']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'type', 'price', 'country_of_origin', 'discount_percent']
    list_filter = ['type', 'country_of_origin']
    search_fields = ['name']


@admin.register(Scientific)
class ScientificAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'button_text']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_filter = ['title']