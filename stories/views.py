from django.db.models import F, ExpressionWrapper, fields, Sum
from django.db.models.functions import Now
from django.utils import timezone
from rest_framework.generics import ListAPIView

from .const import HOT_STORY_TOTAL_READS
from .models import Story, ReadingStats
from .pagination import CustomPagination
from .serializers import StorySerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.all()

        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            queryset = queryset.filter(author__id=author_id)

        genre_id = self.request.query_params.get('genre_id', None)
        if genre_id is not None:
            queryset = queryset.filter(storygenre__genre__id=genre_id)

        slug = self.request.query_params.get('slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        is_hot = self.request.query_params.get('is_hot', None)
        if is_hot is not None:
            is_hot = is_hot.lower() == 'true'
            if is_hot:
                hot_stories_ids = ReadingStats.objects.values('story').annotate(
                    total_reads=Sum('read_count')
                ).filter(total_reads__gte=HOT_STORY_TOTAL_READS).values_list('story', flat=True)
                queryset = queryset.filter(id__in=hot_stories_ids)
            else:
                hot_stories_ids = ReadingStats.objects.values('story').annotate(
                    total_reads=Sum('read_count')
                ).filter(total_reads__gte=HOT_STORY_TOTAL_READS).values_list('story', flat=True)
                queryset = queryset.exclude(id__in=hot_stories_ids)

        is_new = self.request.query_params.get('is_new', None)
        if is_new is not None:
            is_new = is_new.lower() == 'true'
            if is_new:
                now = Now()
                date_diff_expr = ExpressionWrapper(now - F('created_date'), output_field=fields.DurationField())
                queryset = queryset.annotate(date_diff=date_diff_expr).filter(
                    date_diff__lte=timezone.timedelta(days=30))
            else:
                now = Now()
                date_diff_expr = ExpressionWrapper(now - F('created_date'), output_field=fields.DurationField())
                queryset = queryset.annotate(date_diff=date_diff_expr).exclude(
                    date_diff__lte=timezone.timedelta(days=30))

        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset
