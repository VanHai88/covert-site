# Generated by Django 2.2.8 on 2020-03-23 01:52

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='testimonials',
            field=wagtail.core.fields.StreamField([('testimonials', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Name')), ('text', wagtail.core.blocks.CharBlock(label='Item')), ('title', wagtail.core.blocks.CharBlock(label='Item'))]))], default=''),
            preserve_default=False,
        ),
    ]