from django.db.models import Count, Sum, Case, When, Value, BooleanField, Avg, Q
from django.db.models.functions import Now, Round
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from story_site.pagination import CustomPagination
from .const import HOT_STORY_TOTAL_READS, NEW_STORY_DIFF_DATE
from .models import Story
from .serializers import StorySerializer, StoryQueryParameterSerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.select_related("author")

        param_serializer = StoryQueryParameterSerializer(data=self.request.query_params)
        param_serializer.is_valid(raise_exception=True)
        validated_data = param_serializer.validated_data

        queryset = queryset.annotate(
            total_chapters=Count('chapter', distinct=True),
            total_reads=Sum('readingstats__read_count', distinct=True),
            is_new=Case(
                When(created_date__gte=Now() - timezone.timedelta(days=NEW_STORY_DIFF_DATE), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_hot=Case(
                When(total_reads__gte=HOT_STORY_TOTAL_READS, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            avg_rating=Round(Avg('rating__rating_value'), 2),
        )

        filters = Q()

        if 'author_id' in validated_data:
            filters &= Q(author__id=validated_data['author_id'])

        if 'genre_id' in validated_data:
            filters &= Q(storygenre__genre__id=validated_data['genre_id'])

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
        queryset = Story.objects.annotate(
            total_chapters=Count('chapter', distinct=True),
            total_reads=Sum('readingstats__read_count', distinct=True),
            is_new=Case(
                When(created_date__gte=Now() - timezone.timedelta(days=NEW_STORY_DIFF_DATE), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_hot=Case(
                When(total_reads__gte=HOT_STORY_TOTAL_READS, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            avg_rating=Round(Avg('rating__rating_value'), 2),
        )
        story = get_object_or_404(queryset, slug=slug)
        return story
