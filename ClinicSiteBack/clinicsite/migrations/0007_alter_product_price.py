# Generated by Django 4.2.9 on 2024-02-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicsite', '0006_alter_scientific_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена'),
        ),
    ]