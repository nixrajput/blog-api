# Generated by Django 3.1.1 on 2020-09-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200907_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Timestamp'),
        ),
    ]
