# Generated by Django 2.2.8 on 2020-03-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_reg_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='reg_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
