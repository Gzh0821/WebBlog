# Generated by Django 4.0.6 on 2022-07-14 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '栏目',
                'verbose_name_plural': '栏目',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ArticleStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('overview', models.CharField(blank=True, max_length=100)),
                ('text', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('if_publish', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('column', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='article.articlecolumn')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-created_time', 'author'],
            },
        ),
    ]
