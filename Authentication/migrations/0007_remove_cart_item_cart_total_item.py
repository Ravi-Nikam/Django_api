# Generated by Django 5.0.6 on 2024-07-04 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_alter_cart_item_cart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='cart_total_item',
        ),
    ]
