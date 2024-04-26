from django.db import models
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание')
    detailed_description = models.TextField(verbose_name='Подробное описание')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    TYPE_CHOICES = (
        ('supplement', 'БАДы'),
        ('medicine', 'Препараты'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Тип')
    discount_percent = models.IntegerField(verbose_name='Процент скидки')
    country_of_origin = models.CharField(max_length=100, verbose_name='Страна происхождения')
    photo1 = models.ImageField(upload_to='products/', null=True, verbose_name='Фото 1')
    photo2 = models.ImageField(upload_to='products/', null=True, verbose_name='Фото 2')
    photo3 = models.ImageField(upload_to='products/', null=True, verbose_name='Фото 3')
    photo4 = models.ImageField(upload_to='products/', null=True, verbose_name='Фото 4')
    photo5 = models.ImageField(upload_to='products/', null=True, verbose_name='Фото 5')

    brand = models.CharField(max_length=255, null=True, verbose_name='Бренд')
    active_substance = models.CharField(max_length=60, null=True, verbose_name='Действующее вещество')
    release_form = models.CharField(max_length=60, null=True, verbose_name='Форма выпуска')
    amount_in_a_package = models.IntegerField(null=True, verbose_name='Количество в упаковке')
    dosage = models.CharField(max_length=60, null=True, verbose_name='Дозировка')
    purpose = models.CharField(max_length=60, null=True, verbose_name='Назначение')

    warning = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Предупреждение')
    compound = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Состав')
    description = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Описание')
    pharmachologic_effect = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Фармакологический эффект')

    indications_for_use = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Показания к применению')
    contraindications = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Противопоказания')
    side_effects = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Побочные действия')
    course_of_administration_and_dosage = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Курс приема и дозировка')
    conditions_for_dispensing_from_pharmacies = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Условия отпуска из аптек')
    storage_conditions = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Условия хранения')
    special_instructions = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Специальные указания')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_page', args=[str(self.id)])

    def price_with_discount(self):
        if self.discount_percent > 0:
            discount_factor = Decimal(1) - (Decimal(self.discount_percent) / Decimal(100))
            discounted_price = self.price * discount_factor

            # Округляем до ближайшего целого числа
            return discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return self.price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'




class Scientific(models.Model):
    name = models.CharField(max_length=70, verbose_name="Название")
    button_text=models.CharField(max_length=85, verbose_name="Текст для кнопки")
    scientific_text=models.CharField(max_length=300, verbose_name="Описание научной деятельности")
    doc_photo = models.ImageField(upload_to='scientific/', null=True, verbose_name="Фото патента")

    class Meta:
        verbose_name = 'Научная деятельность'
        verbose_name_plural = 'Научную деятельность'


class Certificates(models.Model):
    title = models.CharField(max_length=30, verbose_name="Название")
    short_text = models.CharField(max_length=100, verbose_name="Краткое описание")
    certificate_photo = models.ImageField(upload_to='certificate/', null=True, verbose_name="Фото сертификата")

    class Meta:
        verbose_name = 'Сертификаты'
        verbose_name_plural = 'Сертификат'


class Service(models.Model):
    photo = models.ImageField(upload_to='services_photos/', verbose_name="Фото")
    price = models.CharField(max_length=255, verbose_name="Цена")
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    tag = models.CharField(max_length=100, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"