# Generated by Django 3.2.9 on 2022-01-12 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0026_alter_completed_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completed',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='completed',
            name='order_no',
        ),
        migrations.RemoveField(
            model_name='completed',
            name='paid_order',
        ),
        migrations.RemoveField(
            model_name='completed',
            name='pay_code',
        ),
    ]
