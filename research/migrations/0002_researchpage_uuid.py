# Generated by Django 2.2.8 on 2020-03-31 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchpage',
            name='uuid',
            field=models.CharField(default='', max_length=50, verbose_name='UUID'),
        ),
    ]
