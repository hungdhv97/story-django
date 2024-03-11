from math import ceil

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .consts import NEW_STORY_DIFF_DATE
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
    total_chapters = serializers.IntegerField(read_only=True)
    total_reads = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_hot = serializers.BooleanField(read_only=True)
    avg_rating = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    latest_chapter = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'author', 'genres', 'total_chapters', 'total_reads', 'created_date', 'status',
            'source', 'cover_photo', 'is_new', 'is_hot', 'avg_rating', 'slug', 'latest_chapter'
        ]

    def get_total_chapters(self, story):
        return story.chapter_set.count()

    def get_is_new(self, story):
        created_date = timezone.localtime(story.created_date)
        diff_days_ago = timezone.now() - timezone.timedelta(days=NEW_STORY_DIFF_DATE)
        return created_date >= diff_days_ago

    def get_cover_photo(self, story):
        return story.cover_photo.url

    def get_genres(self, story):
        return GenreSerializer(story.genres, many=True).data

    def get_latest_chapter(self, story):
        if story.latest_chapter_info:
            latest_chapter = story.latest_chapter_info[0]
            return ChapterInStorySerializer(latest_chapter).data
        return None

    def get_total_reads(self, story):
        return story.total_reads[0] if story.total_reads else 0

    def get_avg_rating(self, story):
        return ceil(story.rating_set.aggregate(avg_rating=Avg('rating_value'))['avg_rating'] or 0)


class TopStorySerializer(serializers.ModelSerializer):
    total_reads = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'title', 'cover_photo', 'slug', 'total_reads')

    def get_total_reads(self, story):
        return getattr(story, 'total_reads', 0)

    def get_cover_photo(self, story):
        return story.cover_photo.url if story.cover_photo else None


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
        fields = ['id', 'story', 'number_chapter', 'title', 'content', 'published_date']


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
