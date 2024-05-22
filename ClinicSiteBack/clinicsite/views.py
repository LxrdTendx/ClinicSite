from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView
from math import ceil
from .models import Product, Scientific, Certificates, Service, Profile, Note, Event, TreatmentCourse, Organ
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import Q
from .forms import ProfileForm
from django.contrib import messages



def logout_view(request):
    logout(request)
    return redirect('auth')

def auth_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('profile-admin')  # Перенаправляем персонал на страницу администрирования
        else:
            return redirect('profile')  # Обычные пользователи попадают на свой профиль

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('profile-admin')
            else:
                return redirect('profile')
        else:
            return render(request, 'auth.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'auth.html')

@login_required
def profile_view(request):
    if request.user.is_staff:
        return redirect('profile-admin')

    try:
        profile = request.user.profile
        # Получаем курсы лечения для пользователя
        treatment_courses = TreatmentCourse.objects.filter(user=request.user)
        # Извлекаем все продукты из этих курсов лечения
        products = Product.objects.filter(treatmentcourse__in=treatment_courses).distinct()
    except Profile.DoesNotExist:
        profile = None
        products = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')  # Убедитесь, что у вас есть URL с именем 'profile'
    else:
        form = ProfileForm(instance=profile)

    notes = Note.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'profile.html', {
        'profile': profile,
        'form': form,
        'notes': notes,
        'events': events,
        'products': products  # Передаем продукты в контекст
    })


@login_required
def profile_admin_view(request):
    if not request.user.is_staff:
        return redirect('profile')  # Не-персонал перенаправляется на обычную страницу профиля
    profile = request.user.profile
    # Здесь реализация страницы для персонала
    return render(request, 'profile-admin.html', {'profile': profile})

def login_view(request):
    return render(request, 'login.html')

def service_view(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})



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
    certificates = list(Certificates.objects.all())

    # Вычисляем количество слотов для сертификатов, учитывая заголовок
    total_slots = len(certificates) + 1  # +1 для заголовка

    # Равномерно распределяем сертификаты по трем колонкам
    slots_per_column = [total_slots // 3 + (1 if i < total_slots % 3 else 0) for i in range(3)]

    # Первая колонка имеет на один слот меньше из-за заголовка
    slots_per_column[0] -= 1

    # Определяем индексы начала для каждой колонки
    first_col_end = slots_per_column[0]
    second_col_end = first_col_end + slots_per_column[1]

    # Выделяем сертификаты для каждой колонки
    first_col_certs = certificates[:first_col_end]
    second_col_certs = certificates[first_col_end:second_col_end]
    third_col_certs = certificates[second_col_end:]

    context = {
        'scientific': scientific,
        'first_col_certs': first_col_certs,
        'second_col_certs': second_col_certs,
        'third_col_certs': third_col_certs,
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

@login_required
def refactor_patient_view(request):
    if not request.user.is_staff:
        return redirect('profile')

    profiles = Profile.objects.filter(user__is_staff=False)
    organs = Organ.objects.all()
    selected_profile = None

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        full_name = request.POST.get('full_name')
        diagnosis = request.POST.get('diagnosis')
        organs_ids = request.POST.getlist('organs')
        note_ids = request.POST.getlist('note_ids')
        note_titles = request.POST.getlist('note_titles')
        note_descriptions = request.POST.getlist('note_descriptions')
        delete_note_ids = request.POST.getlist('delete_note_ids')

        profile = get_object_or_404(Profile, id=patient_id)
        profile.full_name = full_name
        profile.diagnosis = diagnosis
        profile.organs.clear()
        profile.organs.add(*organs_ids)
        profile.save()

        for note_id in delete_note_ids:
            Note.objects.filter(id=note_id).delete()

        # Обработка заметок
        for note_id, title, description in zip(note_ids, note_titles, note_descriptions):
            if note_id:
                note = Note.objects.get(id=note_id)
                note.title = title
                note.note_description = description
                note.save()
            else:
                # Создание новой заметки, если id пуст
                if title or description:
                    Note.objects.create(user=profile.user, title=title, note_description=description)

        return redirect('refactor_patient')  # или другой URL для результата
    elif request.method == 'GET' and request.GET.get('patient_id'):
        selected_profile = get_object_or_404(Profile, id=request.GET['patient_id'])

    return render(request, 'refactor_patient.html', {
        'profiles': profiles,
        'organs': organs,
        'selected_profile': selected_profile or profiles.first() if profiles.exists() else None
    })


@login_required
def get_patient_data(request):
    if not request.user.is_staff:
        return redirect('profile')
    patient_id = request.GET.get('patient_id')
    if patient_id:
        profile = Profile.objects.filter(id=patient_id).select_related('user').first()
        if profile:
            organs = profile.organs.values_list('id', flat=True)
            notes = list(profile.user.note_set.values('id', 'title', 'note_description'))
            events = list(Event.objects.filter(user=profile.user).order_by('date', 'time').values('id', 'name', 'date', 'time', 'description'))
            treatment_course = TreatmentCourse.objects.filter(user=profile.user).first()
            product_ids = treatment_course.products.values_list('id', flat=True) if treatment_course else []
            return JsonResponse({
                'full_name': profile.full_name,
                'diagnosis': profile.diagnosis,
                'organs': list(organs),
                'notes': notes,
                'events': events,
                'treatment_course': {
                    'products': list(product_ids)
                }
            })
    return JsonResponse({'error': 'Profile not found'}, status=404)


@login_required
def add_event_view(request):
    if not request.user.is_staff:
        return redirect('profile')
    profiles = Profile.objects.filter(user__is_staff=False)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')

        if patient_id and name and date and time:
            patient = Profile.objects.get(id=patient_id)
            Event.objects.create(
                user=patient.user,  # Здесь мы используем patient.user для привязки к пользователю
                name=name,
                date=date,
                time=time,
                description=description
            )
        return redirect('add_event')


    return render(request, 'add_event.html', {
        'profiles': profiles,
    })

@login_required
def delete_event_view(request):
    if not request.user.is_staff:
        return redirect('profile')
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.filter(id=event_id).first()
            if event:
                event.delete()
                return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)



@login_required
def refactor_course_view(request):
    if not request.user.is_staff:
        return redirect('profile')

    profiles = Profile.objects.filter(user__is_staff=False)
    products = Product.objects.all()  # Получение всех продуктов

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        product_ids = request.POST.getlist('product_ids')

        if patient_id:
            patient = Profile.objects.get(id=patient_id)
            treatment_course, created = TreatmentCourse.objects.get_or_create(user=patient.user)
            treatment_course.products.set(product_ids)
            treatment_course.save()

        return redirect('refactor_course')

    return render(request, 'refactor_course.html', {
        'profiles': profiles,
        'products': products
    })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_page.html'


