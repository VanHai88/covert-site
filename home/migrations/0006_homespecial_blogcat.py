# Generated by Django 2.2.8 on 2020-04-05 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogcategory_order'),
        ('home', '0005_homespecial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homespecial',
            name='blogcat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.BlogCategory'),
        ),
    ]