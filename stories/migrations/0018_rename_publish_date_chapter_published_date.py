# Generated by Django 4.2.6 on 2023-12-18 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0017_alter_story_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='publish_date',
            new_name='published_date',
        ),
    ]