from django.utils import timezone
from rest_framework import serializers

from .consts import HOT_STORY_TOTAL_READS, NEW_STORY_DIFF_DAYS
from .models import Story, Author, Genre, Chapter, Rating, ReadingStats


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class ChapterInStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'number_chapter', 'title', 'published_date']


class StorySerializer(serializers.ModelSerializer):
    total_chapters = serializers.IntegerField()
    total_reads = serializers.IntegerField()
    is_new = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField()
    latest_chapter = ChapterInStorySerializer()
    cover_photo = serializers.SerializerMethodField()
    author = AuthorSerializer()
    genres = GenreSerializer(many=True, read_only=True)

    NEW_STORY_CUTOFF_DATE = timezone.now() - timezone.timedelta(days=NEW_STORY_DIFF_DAYS)

    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'author', 'genres', 'total_chapters', 'total_reads', 'created_date', 'status',
            'source', 'cover_photo', 'is_new', 'is_hot', 'avg_rating', 'slug', 'latest_chapter'
        ]

    def get_cover_photo(self, story):
        return story.cover_photo.url

    def get_is_new(self, story):
        created_date = timezone.localtime(story.created_date)
        diff_days_ago = self.NEW_STORY_CUTOFF_DATE
        return created_date >= diff_days_ago

    def get_is_hot(self, story):
        return story.total_reads_week >= HOT_STORY_TOTAL_READS if story.total_reads_week else False


class TopStorySerializer(serializers.ModelSerializer):
    total_reads = serializers.IntegerField()
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'title', 'cover_photo', 'slug', 'total_reads')

    def get_cover_photo(self, story):
        return story.cover_photo.url


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_slug = serializers.CharField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)
    total_chapters_from = serializers.IntegerField(required=False)
    total_chapters_to = serializers.IntegerField(required=False)
    order_by = serializers.CharField(required=False)


class StoryInChapterSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'title', 'slug', 'cover_photo', 'author']

    def get_cover_photo(self, story):
        return story.cover_photo.url


class ChapterSerializer(serializers.ModelSerializer):
    story = StoryInChapterSerializer()

    class Meta:
        model = Chapter
        fields = ['id', 'story', 'number_chapter', 'title', 'content', 'published_date']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'story', 'rating_value']


class ReadingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingStats
        fields = ['id', 'story', 'read_count', 'date']
