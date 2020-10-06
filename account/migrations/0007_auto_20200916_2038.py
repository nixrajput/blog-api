# Generated by Django 3.1.1 on 2020-09-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0006_account_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Username'),
        ),
    ]
