# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem

from stories.models import Author, Story, StoryGenre, Chapter, Rating, ReadingStats, Genre


class GenreItem(DjangoItem):
    django_model = Genre


class AuthorItem(DjangoItem):
    django_model = Author


class StoryItem(DjangoItem):
    django_model = Story


class StoryGenreItem(DjangoItem):
    django_model = StoryGenre


class ChapterItem(DjangoItem):
    django_model = Chapter


class RatingItem(DjangoItem):
    django_model = Rating


class ReadingStatsItem(DjangoItem):
    django_model = ReadingStats
