# Generated by Django 5.0 on 2023-12-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_shippingaddress_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateField(auto_now_add=True),
        ),
    ]
