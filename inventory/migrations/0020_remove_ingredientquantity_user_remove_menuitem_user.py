# Generated by Django 4.0.2 on 2022-04-15 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_menuitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientquantity',
            name='user',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='user',
        ),
    ]
