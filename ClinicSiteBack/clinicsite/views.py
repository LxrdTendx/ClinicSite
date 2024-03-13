from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView

from .models import Product, Scientific, Certificates

def login_view(request):
    return render(request, 'login.html')

def cart_view(request):
    product_ids = request.GET.get('ids', '')
    quantities = request.GET.get('quantities', '')

    cart_items = []
    total_sum = 0

    if product_ids and quantities:
        product_ids = [int(id) for id in product_ids.split(',') if id.isdigit()]
        quantities = [int(quantity) for quantity in quantities.split(',') if quantity.isdigit()]
        products = Product.objects.filter(id__in=product_ids)

        for product, quantity in zip(products, quantities):
            discounted_price = product.price_with_discount()
            total_price = discounted_price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': discounted_price,  # Цена за штуку с учетом скидки
                'total_price': total_price,
            })

        total_sum = sum(item['total_price'] for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
    })



def about_view(request):
    scientific = Scientific.objects.all()
    certificates = Certificates.objects.all()
    context ={
        'scientific': scientific,
        'certificates': certificates,
    }
    return render(request, 'about.html', context)


def market_view(request):
    unique_countries = Product.objects.values_list('country_of_origin', flat=True).distinct()
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
    paginator = Paginator(products, 20)  # 8 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Если это AJAX-запрос, возвращаем только карточки товаров
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('product_cards.html', {'products': page_obj}, request=request)
        return JsonResponse({'html': html, 'num_pages': paginator.num_pages})



    # Если это не AJAX-запрос, то возвращаем все товары
    context = {
        'products': page_obj,
        'countries': unique_countries,
    }
    return render(request, 'market.html', context)



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_page.html'
