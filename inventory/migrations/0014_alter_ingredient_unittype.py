# Generated by Django 4.0.2 on 2022-03-27 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_ingredient_unittype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unitType',
            field=models.CharField(choices=[('Grams', 'Grams'), ('Ounces', 'Ounces'), ('Pieces', 'Pieces')], default='Pieces', max_length=200),
        ),
    ]