# Generated by Django 4.2.6 on 2024-01-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0020_remove_chapter_chapter_name_chapter_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=255, unique=True),
        ),
    ]
