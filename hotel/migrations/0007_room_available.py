# Generated by Django 3.2.9 on 2021-11-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_alter_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='available',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
