# Generated by Django 2.2.8 on 2020-02-29 21:56

from django.db import migrations, models
import dmedia.models


class Migration(migrations.Migration):

    dependencies = [
        ('dmedia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='pdf',
            field=models.FileField(upload_to=dmedia.models.gen_file_name),
        ),
    ]
