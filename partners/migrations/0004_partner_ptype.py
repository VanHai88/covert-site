# Generated by Django 2.2.8 on 2020-12-08 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0003_partner_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='ptype',
            field=models.CharField(default='fixed', max_length=50, verbose_name='Partner Type'),
        ),
    ]