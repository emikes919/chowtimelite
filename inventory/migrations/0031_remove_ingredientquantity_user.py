# Generated by Django 4.0.2 on 2022-05-26 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_ingredientquantity_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientquantity',
            name='user',
        ),
    ]
