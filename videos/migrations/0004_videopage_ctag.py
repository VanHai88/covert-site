# Generated by Django 2.2.8 on 2020-02-21 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20200202_0549'),
        ('videos', '0003_auto_20200204_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='videopage',
            name='ctag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='utils.Tag'),
            preserve_default=False,
        ),
    ]
