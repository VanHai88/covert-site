# Generated by Django 2.2.8 on 2020-02-06 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200206_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='event',
            name='lng',
        ),
    ]
