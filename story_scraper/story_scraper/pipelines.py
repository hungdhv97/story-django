# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from stories.models import Genre


class StoryScraperPipeline:
    def __init__(self):
        Genre.objects.all().delete()

    def process_item(self, item, spider):
        item.save()
        return item
