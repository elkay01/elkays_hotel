# Generated by Django 3.2.9 on 2021-11-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0010_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
