# Generated by Django 4.0.2 on 2022-04-16 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_ingredientquantity_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientquantity',
            name='user',
        ),
    ]
