# Generated by Django 3.2.8 on 2021-11-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_cartproduct_final_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Общая цена'),
        ),
    ]