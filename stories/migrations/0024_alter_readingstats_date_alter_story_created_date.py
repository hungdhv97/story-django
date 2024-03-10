# Generated by Django 4.2.6 on 2024-03-10 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0023_chapter_number_chapter_alter_readingstats_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingstats',
            name='date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='created_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
