# Generated by Django 4.2.14 on 2024-10-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_model',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
