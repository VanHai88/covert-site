# Generated by Django 2.2.8 on 2020-03-16 03:33

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='countries',
            field=django_countries.fields.CountryField(default='', max_length=746, multiple=True),
            preserve_default=False,
        ),
    ]