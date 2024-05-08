import math
import random
import re
from datetime import timedelta

from django.utils import timezone
from scrapy import Request

from stories.models import (
    Author,
    Chapter,
    Genre,
    Rating,
    ReadingStats,
    Status,
    Story,
    StoryGenre,
)


class ChapterHandler:
    def __init__(self, story, base_url, from_chapter_index, to_chapter_index):
        self.story = story
        self.base_url = base_url
        self.from_chapter_index = from_chapter_index
        self.to_chapter_index = to_chapter_index
        self.chapters_per_page = None
        self.last_page = None

    def start_requests(self):
        yield Request(url=self.base_url.format(1), callback=self.parse_initial)

    def parse_initial(self, response):
        chapters = response.css('.col-truyen-main #list-chapter .row ul li a::attr(href)')
        self.chapters_per_page = len(chapters)
        self.last_page = self.get_last_page(response)
        from_page = math.ceil(self.from_chapter_index / self.chapters_per_page)
        yield Request(url=self.base_url.format(from_page), callback=self.parse)

    def parse(self, response):
        page_number = int(response.url.split('trang-')[-1].split('/')[0])
        start_index_on_page = (self.from_chapter_index - 1) % self.chapters_per_page if page_number == math.ceil(
            self.from_chapter_index / self.chapters_per_page
        ) else 0
        end_index_on_page = (self.to_chapter_index - 1) % self.chapters_per_page if page_number == math.ceil(
            self.to_chapter_index / self.chapters_per_page
        ) else (self.chapters_per_page - 1)

        chapter_urls = response.css('.col-truyen-main #list-chapter .row ul li a::attr(href)').getall()
        for chapter_url in chapter_urls[start_index_on_page:end_index_on_page + 1]:
            yield response.follow(chapter_url, callback=self.parse_chapter)

        if page_number * self.chapters_per_page < self.to_chapter_index and page_number < self.last_page:
            yield Request(url=self.base_url.format(page_number + 1), callback=self.parse)

    def parse_chapter(self, response):
        self.save_chapter(response)

    def save_chapter(self, response):
        title = ''.join(response.css(".chapter-title ::text").getall()).replace('\u200B', '')
        match = re.search(r'Chương (\d+)', title)
        number_chapter = int(match.group(1)) if match else None
        content = "\n".join(response.css(".chapter-c ::text").getall()).replace("\u00A0", " ")
        published_date = timezone.now()
        existing_chapter = Chapter.objects.filter(story_id=self.story.id, title=title).first()
        if existing_chapter is not None:
            return existing_chapter
        chapter = Chapter(
            story_id=self.story.id, number_chapter=number_chapter, title=title, content=content,
            published_date=published_date
        )
        chapter.save()
        print(chapter.id)
        self.update_story_latest_chapter(chapter)
        return chapter

    def update_story_latest_chapter(self, chapter):
        story = chapter.story
        latest_chapter = story.latest_chapter
        if latest_chapter and latest_chapter.number_chapter >= chapter.number_chapter:
            return
        story.latest_chapter = chapter
        story.save(update_fields=['latest_chapter'])

    def get_last_page(self, response):
        last_page_url = response.css("#list-chapter .pagination li a:contains('Cuối ')::attr(href)").get()
        if not last_page_url:
            all_page_urls = response.css("#list-chapter .pagination li a::attr(href)").getall()
            if all_page_urls and len(all_page_urls) > 1:
                last_page_url = all_page_urls[-2]
        if last_page_url:
            last_page_str = last_page_url.split('trang-')[-1].split('/')[0]
            if last_page_str.isdigit():
                return int(last_page_str)
        return -1


class StoryHandler:
    def __init__(self, from_chapter_index, to_chapter_index):
        self.from_chapter_index = from_chapter_index
        self.to_chapter_index = to_chapter_index

    def parse_story(self, response):
        genres = self.save_genres(response)
        author = self.save_author(response)
        story = self.save_story(response, author)
        self.save_story_genres(story, genres)
        self.save_rating(response, story)
        self.save_reading_stats(response, story)
        chapter_base_url = response.url + 'trang-{}'
        chapter_handler = ChapterHandler(story, chapter_base_url, self.from_chapter_index, self.to_chapter_index)
        yield from chapter_handler.start_requests()

    def save_genres(self, response):
        list_genres = []
        genres = response.css('.col-truyen-main .info-holder .info a[itemprop="genre"]::text').getall()
        for genre in genres:
            existing_genre = Genre.objects.filter(name=genre.strip()).first()
            if existing_genre is not None:
                list_genres.append(existing_genre)
            else:
                genre = Genre(name=genre)
                genre.save()
                list_genres.append(genre)
        return list_genres

    def save_author(self, response):
        author_name = response.css('.col-truyen-main .info-holder .info a[itemprop="author"]::text').get()
        existing_author = Author.objects.filter(name=author_name.replace('\u200B', '').strip()).first()
        if existing_author is not None:
            return existing_author
        author = Author(name=author_name)
        author.save()
        return author

    def save_story(self, response, author):
        title = response.css('.col-truyen-main h3.title::text').get()
        shorten_title = title[:title.find('(')].strip() if title.find('(') != -1 else title.strip()
        description = re.sub(
            r'<[^>]+>',
            '',
            re.sub(
                r'<br\s*/?>',
                '\n',
                response.css('.col-truyen-main .desc-text').get()
            )
        ).replace("\u00A0", " ")
        created_date = timezone.now() - timedelta(days=60) + timedelta(days=random.randint(0, 60))
        # Mapping of conditions to statuses
        status_ongoing = response.css('.col-truyen-main .info-holder .info span.text-primary::text').get()
        status_success = response.css('.col-truyen-main .info-holder .info span.text-success::text').get()
        status_conditions = {
            Status.ONGOING: status_ongoing is not None,
            Status.COMPLETED: status_success is not None,
        }
        # Find the first true condition and set the status, default to DROPPED
        status = next((status for status, condition in status_conditions.items() if condition), Status.DROPPED)
        story_source = response.css('.col-truyen-main .info-holder .info span.source::text').get()
        source = story_source or ""
        cover_photo = response.css('.col-truyen-main .info-holder img::attr(src)').get()

        existing_story = Story.objects.filter(title=shorten_title).first()
        if existing_story is not None:
            return existing_story
        story = Story(
            title=shorten_title, description=description, author_id=author.id, created_date=created_date,
            status=status,
            source=source, cover_photo=cover_photo
        )
        story.save()
        return story

    def save_story_genres(self, story, genres):
        for genre in genres:
            existing_story_genre = StoryGenre.objects.filter(story_id=story.id, genre_id=genre.id).first()
            if existing_story_genre is None:
                story_genre = StoryGenre(story_id=story.id, genre_id=genre.id)
                story_genre.save()

    def save_rating(self, response, story):
        rating_value = round(
            float(response.css(".col-truyen-main .desc .rate .small span[itemprop='ratingValue']::text").get()) / 2
        )

        existing_rating = Rating.objects.filter(story_id=story.id).first()
        if existing_rating is None:
            rating = Rating(story_id=story.id, rating_value=rating_value)
            rating.save()

    def save_reading_stats(self, response, story):
        today = timezone.now()
        two_months_ago = today - timedelta(days=60)
        for single_date in (two_months_ago + timedelta(n) for n in range((today - two_months_ago).days)):
            read_count = random.randint(100, 100000)
            existing_reading_stats = ReadingStats.objects.filter(story_id=story.id, date=single_date).first()
            if existing_reading_stats is None:
                reading_stats = ReadingStats(story_id=story.id, read_count=read_count, date=single_date)
                reading_stats.save()
