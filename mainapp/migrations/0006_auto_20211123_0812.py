# Generated by Django 3.2.8 on 2021-11-23 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_remove_cartproduct_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartProduct',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]