# Generated by Django 4.2.6 on 2023-10-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stories', '0015_rename_genre_id_storygenre_genre_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='readingstats',
            name='reading_stats_idx',
        ),
        migrations.RemoveIndex(
            model_name='storygenre',
            name='story_genre_idx',
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='story_id',
            new_name='story',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='story_id',
            new_name='story',
        ),
        migrations.RenameField(
            model_name='readingstats',
            old_name='story_id',
            new_name='story',
        ),
        migrations.AlterUniqueTogether(
            name='readingstats',
            unique_together={('story', 'date')},
        ),
        migrations.AddIndex(
            model_name='readingstats',
            index=models.Index(fields=['story', 'date'], name='reading_stats_idx'),
        ),
        migrations.AddIndex(
            model_name='storygenre',
            index=models.Index(fields=['story', 'genre'], name='story_genre_idx'),
        ),
    ]