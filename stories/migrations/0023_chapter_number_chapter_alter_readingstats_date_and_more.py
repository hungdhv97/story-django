# Generated by Django 4.2.6 on 2024-03-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0022_alter_chapter_published_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='number_chapter',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='readingstats',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='created_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('dropped', 'Dropped')], db_index=True, default='ongoing', max_length=9),
        ),
    ]