# Generated by Django 4.2.6 on 2023-10-13 10:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('stories', '0013_story_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='genres',
        ),
    ]
