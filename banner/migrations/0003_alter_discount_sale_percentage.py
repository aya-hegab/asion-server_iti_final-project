# Generated by Django 5.0.2 on 2024-03-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='sale_percentage',
            field=models.IntegerField(),
        ),
    ]
