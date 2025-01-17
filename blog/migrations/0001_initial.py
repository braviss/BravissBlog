# Generated by Django 5.0.1 on 2024-03-17 12:31

import django.db.models.deletion
import django.utils.timezone
import tinymce.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modify_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modify_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('body', tinymce.models.HTMLField()),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, default='article_img/default_article.svg', null=True, upload_to='article_img')),
                ('status', models.CharField(choices=[('pe', 'Pending'), ('pu', 'Published'), ('re', 'Rejected')], default='pe', max_length=2)),
                ('views', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'db_table_comment': 'Article table braviss',
                'get_latest_by': 'created_at',
            },
        ),
    ]
