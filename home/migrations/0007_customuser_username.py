# Generated by Django 5.1.7 on 2025-03-07 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
