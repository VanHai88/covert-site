# Generated by Django 2.2.8 on 2020-02-01 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='contact',
            field=models.CharField(default='', max_length=50, verbose_name='Contact'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
