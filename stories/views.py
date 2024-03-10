from datetime import datetime, timedelta

from django.db.models import Case, When, BooleanField, Q
from django.db.models import IntegerField
from django.db.models import Sum, OuterRef, Subquery
from django.db.models import Value
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from story_site.pagination import CustomPagination
from .models import Story, Chapter, Genre, ReadingStats, Author
from .serializers import StorySerializer, StoryQueryParameterSerializer, ChapterSerializer, RatingSerializer, \
    GenreSerializer, ChapterInStorySerializer, TopStorySerializer, AuthorSerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.select_related("author")
        param_serializer = StoryQueryParameterSerializer(data=self.request.query_params)
        param_serializer.is_valid(raise_exception=True)
        validated_data = param_serializer.validated_data

        filters = Q()

        if 'author_id' in validated_data:
            filters &= Q(author__id=validated_data['author_id'])

        if 'genre_slug' in validated_data:
            filters &= Q(storygenre__genre__slug=validated_data['genre_slug'])

        if 'is_hot' in validated_data and validated_data['is_hot'] is True:
            queryset = queryset.annotate(
                is_hot=Case(
                    When(
                        readingstats__date__gte=timezone.now() - timedelta(days=7),
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )

            filters &= Q(is_hot=True)
        if 'is_new' in validated_data and validated_data['is_new'] is True:
            filters &= Q(is_new=True)

        if 'status' in validated_data:
            filters &= Q(status=validated_data['status'])

        if 'total_chapters_from' in validated_data:
            filters &= Q(total_chapters__gte=validated_data['total_chapters_from'])

        if 'total_chapters_to' in validated_data:
            filters &= Q(total_chapters__lte=validated_data['total_chapters_to'])

        queryset = queryset.filter(filters)

        if 'total_chapters_from' in validated_data or 'total_chapters_to' in validated_data:
            queryset = queryset.order_by('-total_chapters')

        return queryset


class StoryDetailView(RetrieveAPIView):
    serializer_class = StorySerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug', None)
        queryset = Story.objects.all()
        story = get_object_or_404(queryset, slug=slug)
        return story


class ChapterListView(ListAPIView):
    serializer_class = ChapterSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Chapter.objects.filter(story__slug=slug).select_related('story')

        sort = self.request.query_params.get('sort')
        if sort == 'desc':
            queryset = queryset.order_by('-number_chapter')
        else:
            queryset = queryset.order_by('number_chapter')

        return queryset


class ChapterShortInfoListView(ListAPIView):
    serializer_class = ChapterInStorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        story = get_object_or_404(Story, slug=slug)
        queryset = Chapter.objects.filter(story=story)

        sort = self.request.query_params.get('sort')
        if sort == 'desc':
            queryset = queryset.order_by('-number_chapter')
        else:
            queryset = queryset.order_by('number_chapter')

        return queryset


class ChapterDetailView(RetrieveAPIView):
    serializer_class = ChapterSerializer
    lookup_field = 'id'

    def get_object(self):
        chapter_id = self.kwargs.get('chapter_id')
        chapter = get_object_or_404(Chapter, id=chapter_id)
        return chapter


class RatingCreateView(CreateAPIView):
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class GenreListView(ListAPIView):
    serializer_class = GenreSerializer
    pagination_class = None
    queryset = Genre.objects.all()


class GenreDetailView(RetrieveAPIView):
    serializer_class = GenreSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        genre = get_object_or_404(Genre, slug=slug)
        return genre


class AuthorDetailView(RetrieveAPIView):
    serializer_class = AuthorSerializer
    lookup_field = 'id'

    def get_object(self):
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(Author, id=author_id)
        return author


class StorySearchView(ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        text = self.request.query_params.get('text', '')
        queryset = Story.objects.filter(
            Q(title__icontains=text) |
            Q(author__name__icontains=text)
        )[:5]
        return queryset


class TopStoryListView(APIView):
    def get(self, request, *args, **kwargs):
        one_week_ago = datetime.now() - timedelta(days=7)
        one_month_ago = datetime.now() - timedelta(days=30)

        reads_in_last_week = ReadingStats.objects.filter(
            story=OuterRef('pk'),
            date__gte=one_week_ago
        ).values('story').annotate(
            total=Sum('read_count')
        ).values('total')
        reads_in_last_month = ReadingStats.objects.filter(
            story=OuterRef('pk'),
            date__gte=one_month_ago
        ).values('story').annotate(
            total=Sum('read_count')
        ).values('total')

        top_week_stories = Story.objects.annotate(
            total_reads=Subquery(reads_in_last_week, output_field=IntegerField())
        ).order_by('-total_reads')[:10]
        top_month_stories = Story.objects.annotate(
            total_reads=Subquery(reads_in_last_month, output_field=IntegerField())
        ).order_by('-total_reads')[:10]
        top_all_time_stories = Story.objects.annotate(
            total_reads=Sum('readingstats__read_count', distinct=True)
        ).order_by('-total_reads')[:10]

        week_data = TopStorySerializer(top_week_stories, many=True).data
        month_data = TopStorySerializer(top_month_stories, many=True).data
        all_time_data = TopStorySerializer(top_all_time_stories, many=True).data

        return Response({
            "week": week_data,
            "month": month_data,
            "all": all_time_data,
        })
