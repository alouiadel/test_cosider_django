# Generated by Django 5.0.2 on 2024-03-03 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='total_price_ht',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
