from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from story_scraper.story_scraper import settings
from story_scraper.story_scraper.spiders.list_stories_spider import ListStoriesSpider

from_story_index = 105
to_story_index = 106
from_chapter_index = 1
to_chapter_index = 1000
crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(
    ListStoriesSpider,
    from_story_index=from_story_index,
    to_story_index=to_story_index,
    from_chapter_index=from_chapter_index,
    to_chapter_index=to_chapter_index
)
process.start()
