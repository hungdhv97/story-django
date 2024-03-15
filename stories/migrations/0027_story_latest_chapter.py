# Generated by Django 4.2.6 on 2024-03-14 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0026_story_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='latest_chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='latest_chapter', to='stories.chapter'),
        ),
    ]