# Generated by Django 4.1 on 2022-08-27 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_unit',
            field=models.IntegerField(default=0),
        ),
    ]