# Generated by Django 4.0.2 on 2022-05-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_alter_ingredient_inventoryquantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='inventoryQuantity',
            field=models.IntegerField(max_length=200, verbose_name='Quantity'),
        ),
    ]
