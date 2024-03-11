# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from django.db import connection

from stories.models import Genre, Author, StoryGenre, Rating, ReadingStats, Story


class ClearDatabasePipeline:
    def open_spider(self, spider):
        self.clear_database()
        self.reset_auto_increment_stories()

    def clear_database(self):
        Genre.objects.all().delete()
        Author.objects.all().delete()
        Story.objects.all().delete()
        StoryGenre.objects.all().delete()
        Rating.objects.all().delete()
        ReadingStats.objects.all().delete()

    def reset_auto_increment_stories(self):
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                # Query to get sequences starting with 'stories'
                cursor.execute("SELECT c.relname FROM pg_class c WHERE c.relkind = 'S' AND c.relname LIKE 'stories%';")
                sequences = cursor.fetchall()
                # Reset each sequence
                for seq in sequences:
                    cursor.execute(f"ALTER SEQUENCE {seq[0]} RESTART WITH 1;")
            elif connection.vendor == 'sqlite':
                # Delete entries for tables starting with 'stories' in sqlite_sequence
                cursor.execute("DELETE FROM sqlite_sequence WHERE name LIKE 'stories%';")
                cursor.execute('VACUUM;')
