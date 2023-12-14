import scrapy

from story_scraper.story_scraper.items import AuthorItem


class AuthorSpider(scrapy.Spider):
    name = 'author_spider'
    allowed_domains = ['truyenfull.vn']
    start_urls = ['https://truyenfull.vn/danh-sach/truyen-hot/']

    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.AuthorPipeline": 300,
        }
    }

    def parse(self, response):
        genres = response.css(".list-truyen.list-cat .row a::text").getall()

        for genre in genres:
            genre_item = AuthorItem()
            genre_item['name'] = genre
            yield genre_item
