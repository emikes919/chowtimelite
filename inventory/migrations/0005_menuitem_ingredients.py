# Generated by Django 4.0.2 on 2022-03-09 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_ingredientquantity_alter_menuitem_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='ingredients',
            field=models.ManyToManyField(through='inventory.IngredientQuantity', to='inventory.Ingredient'),
        ),
    ]
