# Generated by Django 4.0.2 on 2022-05-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0032_alter_ingredient_unittype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientquantity',
            name='ingredientQuantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]