# Generated by Django 4.2.6 on 2023-10-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='chapter_count',
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('OG', 'Ongoing'), ('CP', 'Completed'), ('DR', 'Dropped')], default='OG',
                                   max_length=2),
        ),
    ]
