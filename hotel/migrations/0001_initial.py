# Generated by Django 3.2.9 on 2021-11-02 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(default='pix.jpg', upload_to='rooms')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('beds', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField()),
                ('image', models.ImageField(default='pix.jpg', upload_to='rooms')),
                ('description', models.TextField()),
                ('available', models.BooleanField()),
                ('min', models.IntegerField(default=1)),
                ('max', models.IntegerField(default=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.category')),
            ],
        ),
    ]