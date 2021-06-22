# Generated by Django 2.2.8 on 2020-02-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('courses', '0003_auto_20200201_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='tags',
        ),
        migrations.AddField(
            model_name='course',
            name='ctags',
            field=models.ManyToManyField(to='utils.Tag'),
        ),
        migrations.DeleteModel(
            name='CoursePageTag',
        ),
    ]