# Generated by Django 2.2.8 on 2020-03-16 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20200202_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='text',
            field=models.CharField(max_length=300, verbose_name='text'),
        ),
    ]