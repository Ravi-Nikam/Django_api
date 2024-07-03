# Generated by Django 5.0.6 on 2024-07-03 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_remove_product_no_days_remove_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart_item',
            fields=[
                ('cart_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_quantity_item', models.PositiveIntegerField(default=1)),
                ('cart_total_item', models.IntegerField()),
                ('product_cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.product')),
                ('user_cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.cart_item')),
            ],
        ),
    ]
