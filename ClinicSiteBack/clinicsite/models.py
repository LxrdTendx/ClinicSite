from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    detailed_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    TYPE_CHOICES = (
        ('supplement', 'БАДы'),
        ('medicine', 'Препараты'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    discount_percent = models.IntegerField()
    country_of_origin = models.CharField(max_length=100)
    photo1 = models.ImageField(upload_to='products/', null=True)
    photo2 = models.ImageField(upload_to='products/', null=True)
    photo3 = models.ImageField(upload_to='products/', null=True)
    photo4 = models.ImageField(upload_to='products/', null=True)
    photo5 = models.ImageField(upload_to='products/', null=True)
    def __str__(self):
        return self.name
