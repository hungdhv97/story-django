import scrapy

from story_scraper.story_scraper.items import GenreItem


class GenreSpider(scrapy.Spider):
    name = 'genre_spider'
    allowed_domains = ['truyenfull.vn']
    start_urls = ['https://truyenfull.vn/']

    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.ResetAutoIncrementPipeline": 200,
            "story_scraper.story_scraper.pipelines.GenrePipeline": 300,
        }
    }

    def parse(self, response):
        genres = response.css(".list-truyen.list-cat .row a::text").getall()

        for genre in genres:
            genre_item = GenreItem()
            genre_item['name'] = genre
            yield genre_item
