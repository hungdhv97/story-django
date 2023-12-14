# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from django.db import connection

# useful for handling different item types with a single interface
from stories.models import Genre


class GenrePipeline:
    def __init__(self):
        Genre.objects.all().delete()
        self.reset_auto_increment_stories()

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

    def process_item(self, item, spider):
        item.save()
        return item
