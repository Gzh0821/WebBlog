# Generated by Django 4.0.6 on 2023-05-13 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_alter_articlestorage_options'),
        ('userprofile', '0003_profile_collected_com'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='collected_com',
            field=models.ManyToManyField(blank=True, to='article.articlestorage'),
        ),
    ]
