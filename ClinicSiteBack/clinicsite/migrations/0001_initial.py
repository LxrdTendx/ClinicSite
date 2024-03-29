# Generated by Django 4.2.9 on 2024-01-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.TextField()),
                ('detailed_description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('supplement', 'БАДы'), ('medicine', 'Препараты')], max_length=10)),
                ('discount_percent', models.IntegerField()),
                ('country_of_origin', models.CharField(max_length=100)),
                ('photo1', models.ImageField(upload_to='products/')),
                ('photo2', models.ImageField(upload_to='products/')),
                ('photo3', models.ImageField(upload_to='products/')),
                ('photo4', models.ImageField(upload_to='products/')),
                ('photo5', models.ImageField(upload_to='products/')),
            ],
        ),
    ]
