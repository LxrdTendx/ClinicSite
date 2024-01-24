from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product

def login_view(request):
    return render(request, 'login.html')

def about_view(request):
    return render(request, 'about.html')

def market_view(request):
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('sort', 'asc')  # По умолчанию сортируем по возрастанию

    # Получаем все товары и фильтруем по поисковому запросу
    products = Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Сортировка товаров
    if sort_order == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('price')

    # Фильтрация по типам
    product_types = request.GET.getlist('type')
    if product_types:
        products = products.filter(type__in=product_types)

    # Фильтрация по странам
    countries = request.GET.getlist('country')
    if countries:
        products = products.filter(country_of_origin__in=countries)

    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)


    # Установите количество товаров на странице
    paginator = Paginator(products, 6)  # 6 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Если это AJAX-запрос, возвращаем только карточки товаров
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('product_cards.html', {'products': page_obj}, request=request)
        return JsonResponse({'html': html, 'num_pages': paginator.num_pages})



    # Если это не AJAX-запрос, то возвращаем все товары
    context = {
        'products': page_obj,
    }
    return render(request, 'market.html', context)


