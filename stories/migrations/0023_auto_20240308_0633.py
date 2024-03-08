# Generated by Django 4.2.6 on 2024-03-08 06:33
import re

from django.db import migrations, models

from stories.models import Chapter


def extract_chapter_numbers(apps, schema_editor):
    for chapter in Chapter.objects.all():
        try:
            match = re.search(r'Chương (\d+)', chapter.title)
            if match:
                number = int(match.group(1))
                chapter.number_chapter = number
            else:
                chapter.number_chapter = None
        except (ValueError, IndexError):
            chapter.number_chapter = None
        chapter.save()


class Migration(migrations.Migration):
    dependencies = [
        ('stories', '0022_alter_chapter_published_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='number_chapter',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.RunPython(extract_chapter_numbers),
    ]
