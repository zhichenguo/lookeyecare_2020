# Generated by Django 3.0.5 on 2020-05-05 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0011_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='cart',
        ),
    ]