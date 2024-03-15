from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .consts import HOT_STORY_TOTAL_READS, NEW_STORY_DIFF_DAYS
from .models import Story, Author, Genre, Chapter, Rating


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
    total_reads = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'title', 'cover_photo', 'slug', 'total_reads')

    def get_total_reads(self, obj):
        return getattr(obj, 'total_reads', 0)

    def get_cover_photo(self, obj):
        return obj.cover_photo.url if obj.cover_photo else None


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_slug = serializers.CharField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)
    total_chapters_from = serializers.IntegerField(required=False)
    total_chapters_to = serializers.IntegerField(required=False)


class StoryInChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'slug']


class ChapterSerializer(serializers.ModelSerializer):
    story = StoryInChapterSerializer()

    class Meta:
        model = Chapter
        fields = ['id', 'story', 'title', 'content', 'published_date']


class RatingSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Rating
        fields = ['slug', 'rating_value']

    def create(self, validated_data):
        slug = validated_data.pop('slug')
        story = get_object_or_404(Story, slug=slug)
        rating = Rating.objects.create(story=story, **validated_data)
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['slug'] = instance.story.slug
        return representation
