# Generated by Django 3.0.5 on 2020-05-05 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0014_auto_20200505_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='alive',
            field=models.BooleanField(default=False),
        ),
    ]