from django.shortcuts import render

from .models import Product

def login_view(request):
    return render(request, 'login.html')

def about_view(request):
    return render(request, 'about.html')

def market_view(request):
    # Получение продуктов из базы данных
    products = Product.objects.all()

    # Разделение продуктов на два списка для двух разных card-container
    first_three_products = products[:3]
    next_eight_products = products[3:11]

    # Передача продуктов в шаблон
    context = {
        'first_three_products': first_three_products,
        'next_eight_products': next_eight_products
    }
    return render(request, 'market.html', context)