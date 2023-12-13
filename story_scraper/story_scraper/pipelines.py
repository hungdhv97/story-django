# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from stories.models import Genre


class StoryScraperPipeline:
    def __init__(self):
        self.cursor = None
        self.connection = None
        Genre.objects.all().delete()
        self.create_connection()
        self.reindex_all_table()

    def create_connection(self):
        self.connection = sqlite3.connect("data.sqlite3")
        self.cursor = self.connection.cursor()

    def reindex_all_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS sqlite_sequence""")

    def process_item(self, item, spider):
        item.save()
        return item
