# Generated by Django 3.0.5 on 2020-05-05 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_auto_20200504_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='being_delivered',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='received',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='refund_granted',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='refund_requested',
        ),
        migrations.AddField(
            model_name='order',
            name='being_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_billing_address', to='shopping.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.Coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='refund_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='refund_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_shipping_address', to='shopping.Address'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_billing_address', to='shopping.Address'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_shipping_address', to='shopping.Address'),
        ),
    ]