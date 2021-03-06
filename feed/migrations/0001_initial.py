# Generated by Django 2.2.8 on 2020-01-04 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stream_django.activity


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Blocked')], default=1, max_length=20)),
                ('position', models.CharField(choices=[(1, 'Follower'), (2, 'Member'), (3, 'Admin'), (4, 'Creator')], default=1, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StreamGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=50, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(blank=True, upload_to='')),
                ('description', models.TextField(blank=True)),
                ('members', models.ManyToManyField(through='feed.Membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StreamPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.StreamGroup')),
            ],
            bases=(models.Model, stream_django.activity.Activity),
        ),
        migrations.CreateModel(
            name='StreamComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.StreamPost')),
            ],
            bases=(models.Model, stream_django.activity.Activity),
        ),
        migrations.AddField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.StreamGroup'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
