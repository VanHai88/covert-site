# Generated by Django 2.2.8 on 2020-03-13 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old', models.CharField(max_length=300, verbose_name='Old')),
                ('new', models.CharField(max_length=300, verbose_name='New')),
            ],
        ),
    ]
