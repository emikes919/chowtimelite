# Generated by Django 4.0.2 on 2022-03-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_alter_ingredient_unittype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unitType',
            field=models.CharField(choices=[('GR', 'Grams'), ('OZ', 'Ounces'), ('IT', 'Item')], default='IT', max_length=200),
        ),
    ]
