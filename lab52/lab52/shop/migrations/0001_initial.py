# Generated by Django 5.0.4 on 2024-05-13 04:44

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PickupPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['address'],
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('ptype', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['ptype'],
            },
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('expire_date', models.DateTimeField()),
                ('is_used', models.BooleanField()),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Suplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=19, validators=[django.core.validators.RegexValidator('\\+375 \\((29|33|25)\\) \\d{3}-\\d{2}-\\d{2}', message='Phone number must have format +375 (29) XXX-XX-XX ')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=19, validators=[django.core.validators.RegexValidator('\\+375 \\((29|33|25)\\) \\d{3}-\\d{2}-\\d{2}', message='Phone number must have format +375 (29) XXX-XX-XX ')])),
                ('date_of_birth', models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2006, 5, 18), message='You must be 18 or older to use this service')])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2006, 5, 18), message='You must be 18 or older to use this service')])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(editable=False, max_length=10)),
                ('name', models.CharField(max_length=40)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('ptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.producttype')),
                ('supliers', models.ManyToManyField(related_name='products', to='shop.suplier')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('complete_date', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.client')),
                ('pickup_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.pickuppoint')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
                ('promocode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.promocode')),
            ],
            options={
                'ordering': ['complete_date'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
                ('suplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.suplier')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
