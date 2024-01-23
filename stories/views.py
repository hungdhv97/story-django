from datetime import datetime, timedelta

from django.db.models import Count, Case, When, BooleanField, Avg, Q
from django.db.models import IntegerField
from django.db.models import Sum, OuterRef, Subquery
from django.db.models import Value
from django.db.models.functions import Cast
from django.db.models.functions import Now, Round
from django.db.models.functions import StrIndex, Substr, Length, Trim
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from story_site.pagination import CustomPagination
from .consts import HOT_STORY_TOTAL_READS, NEW_STORY_DIFF_DATE
from .models import Story, Chapter, Genre, ReadingStats
from .serializers import StorySerializer, StoryQueryParameterSerializer, ChapterSerializer, RatingSerializer, \
    GenreSerializer, ChapterInStorySerializer, TopStorySerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.select_related("author")

        param_serializer = StoryQueryParameterSerializer(data=self.request.query_params)
        param_serializer.is_valid(raise_exception=True)
        validated_data = param_serializer.validated_data

        one_week_ago = datetime.now() - timedelta(days=7)
        queryset = queryset.annotate(
            total_chapters=Count('chapter', distinct=True),
            total_reads_week=Sum(
                Case(
                    When(readingstats__date__gte=one_week_ago, then='readingstats__read_count'),
                    default=0,
                    output_field=IntegerField(),
                ),
                distinct=True
            ),
            total_reads_all=Sum('readingstats__read_count', distinct=True),
            is_new=Case(
                When(created_date__gte=Now() - timezone.timedelta(days=NEW_STORY_DIFF_DATE), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_hot=Case(
                When(total_reads_week__gte=HOT_STORY_TOTAL_READS, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            avg_rating=Round(Avg('rating__rating_value'), 2),
        )

        filters = Q()

        if 'author_id' in validated_data:
            filters &= Q(author__id=validated_data['author_id'])

        if 'genre_slug' in validated_data:
            filters &= Q(storygenre__genre__slug=validated_data['genre_slug'])

        if 'is_hot' in validated_data and validated_data['is_hot'] is True:
            filters &= Q(is_hot=True)

        if 'is_new' in validated_data and validated_data['is_new'] is True:
            filters &= Q(is_new=True)

        if 'status' in validated_data:
            filters &= Q(status=validated_data['status'])

        queryset = queryset.filter(filters)

        return queryset


class StoryDetailView(RetrieveAPIView):
    serializer_class = StorySerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug', None)
        one_week_ago = datetime.now() - timedelta(days=7)
        queryset = Story.objects.annotate(
            total_chapters=Count('chapter', distinct=True),
            total_reads_week=Sum(
                Case(
                    When(readingstats__date__gte=one_week_ago, then='readingstats__read_count'),
                    default=0,
                    output_field=IntegerField(),
                ),
                distinct=True
            ),
            total_reads_all=Sum('readingstats__read_count', distinct=True),
            is_new=Case(
                When(created_date__gte=Now() - timezone.timedelta(days=NEW_STORY_DIFF_DATE), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_hot=Case(
                When(total_reads_week__gte=HOT_STORY_TOTAL_READS, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            avg_rating=Round(Avg('rating__rating_value'), 2),
        )
        story = get_object_or_404(queryset, slug=slug)
        return story


class ChapterListView(ListAPIView):
    serializer_class = ChapterSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        story = get_object_or_404(Story, slug=slug)
        queryset = Chapter.objects.filter(story=story)

        queryset = queryset.annotate(
            number_chapter=Cast(
                Trim(
                    Substr(
                        'title',
                        StrIndex('title', Value('Chương ')) + 7,
                        Length('title')
                    )
                ),
                IntegerField()
            )
        )

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

        queryset = queryset.annotate(
            number_chapter=Cast(
                Trim(
                    Substr(
                        'title',
                        StrIndex('title', Value('Chương ')) + 7,
                        Length('title')
                    )
                ),
                IntegerField()
            )
        )

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
        chapter_id = self.kwargs.get('chapterId')
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


class StorySearchView(ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        text = self.request.query_params.get('text', '')
        queryset = Story.objects.filter(
            Q(title__icontains=text) |
            Q(author__name__icontains=text)
        )
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
