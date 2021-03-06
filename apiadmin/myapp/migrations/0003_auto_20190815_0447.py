# Generated by Django 2.2.3 on 2019-08-15 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190814_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_male',
            field=models.BooleanField(choices=[(False, 'Female'), (True, 'Male')], verbose_name='gender'),
        ),
    ]
