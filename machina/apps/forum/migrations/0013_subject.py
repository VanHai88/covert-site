# Generated by Django 2.2.8 on 2020-02-13 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_forum_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Subject')),
            ],
        ),
    ]
