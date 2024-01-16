import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Story, Author, Genre, Chapter, StoryGenre, Rating


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class ChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'published_date']


class StorySerializer(serializers.ModelSerializer):
    total_chapters = serializers.IntegerField(read_only=True)
    total_reads = serializers.IntegerField(read_only=True)
    is_new = serializers.BooleanField(read_only=True)
    is_hot = serializers.BooleanField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
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

    def get_cover_photo(self, obj):
        return obj.cover_photo.url

    def get_genres(self, obj):
        story_genres = StoryGenre.objects.filter(story=obj)
        genres = Genre.objects.filter(storygenre__in=story_genres)
        return GenreSerializer(genres, many=True).data

    def get_latest_chapter(self, obj):
        chapters = Chapter.objects.filter(story=obj)
        latest_chapter = None
        highest_number = -1
        for chapter in chapters:
            match = re.search(r'Chương (\d+):', chapter.title)
            if match:
                number = int(match.group(1))
                if number > highest_number:
                    highest_number = number
                    latest_chapter = chapter
        return ChapterDetailSerializer(latest_chapter).data if latest_chapter else None


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_id = serializers.IntegerField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)


class StoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'slug']


class ChapterSerializer(serializers.ModelSerializer):
    story = StoryDetailSerializer()

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
