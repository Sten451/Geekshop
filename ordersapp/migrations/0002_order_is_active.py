# Generated by Django 3.2.7 on 2021-10-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активный'),
        ),
    ]
