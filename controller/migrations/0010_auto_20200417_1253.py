# Generated by Django 3.0.5 on 2020-04-17 16:53

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0009_auto_20200417_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='ref_code'),
        ),
    ]