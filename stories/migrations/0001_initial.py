# Generated by Django 4.2.6 on 2023-10-11 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('chapter_count', models.IntegerField()),
                ('created_date', models.DateField()),
                ('status', models.BooleanField()),
                ('source', models.CharField(max_length=255)),
                ('editor', models.CharField(max_length=255)),
                ('cover_photo', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('slug', models.CharField(max_length=255)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.author')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.IntegerField()),
                ('story_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.IntegerField()),
                ('chapter_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('publish_date', models.DateField()),
                ('story_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
        ),
        migrations.CreateModel(
            name='StoryGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.genre')),
                ('story_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
            options={
                'indexes': [models.Index(fields=['story_id', 'genre_id'], name='story_genre_idx')],
                'unique_together': {('story_id', 'genre_id')},
            },
        ),
        migrations.CreateModel(
            name='ReadingStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_count', models.IntegerField()),
                ('date', models.DateField()),
                ('story_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
            options={
                'indexes': [models.Index(fields=['story_id', 'date'], name='reading_stats_idx')],
                'unique_together': {('story_id', 'date')},
            },
        ),
    ]
