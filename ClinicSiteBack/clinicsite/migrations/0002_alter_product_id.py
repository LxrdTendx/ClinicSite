# Generated by Django 4.2.9 on 2024-01-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
