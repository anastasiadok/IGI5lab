# Generated by Django 5.0.4 on 2024-05-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='complete_date',
            field=models.DateTimeField(null=True),
        ),
    ]