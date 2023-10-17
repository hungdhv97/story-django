from django.db.models import Count, Subquery, OuterRef, Sum, IntegerField, ExpressionWrapper, F, DurationField
from django.db.models.functions import Now
from rest_framework.generics import ListAPIView
from django.utils import timezone
from .models import Story, ReadingStats
from .pagination import CustomPagination
from .serializers import StorySerializer, StoryQueryParameterSerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.select_related("author")

        # Deserialize query parameters
        param_serializer = StoryQueryParameterSerializer(data=self.request.query_params)
        param_serializer.is_valid(raise_exception=True)
        validated_data = param_serializer.validated_data

        now = Now()

        queryset = queryset.annotate(
            total_chapters=Count('chapter'),
            # total_reads=Subquery(
            #
            #     ReadingStats.objects.filter(story=OuterRef('pk')).values('story')
            #     .annotate(total=Sum('read_count')).values('total'),
            #     output_field=IntegerField()
            # ),
            total_reads_2=Sum('readingstats__read_count', distinct=True),
            is_new=ExpressionWrapper(now - F('created_date'), output_field=DurationField()) <= timezone.timedelta(days=30),
            # is_hot=Subquery(
            #     ReadingStats.objects.filter(story=OuterRef('pk')).values('story')
            #     .annotate(total=Sum('read_count')).values('total'),
            #     output_field=models.IntegerField()
            # ) >= 500,
            # rating=Subquery(
            #     Rating.objects.filter(story=OuterRef('pk')).values('story')
            #     .annotate(avg_rating=Avg('rating_value')).values('avg_rating'),
            #     output_field=models.FloatField()
            # ),
            # genres=Subquery(
            #     Genre.objects.filter(storygenre__story=OuterRef('pk')).values('name'),
            #     output_field=models.CharField()
            # ),
            # latest_chapter=Subquery(
            #     Chapter.objects.filter(story=OuterRef('pk')).values('chapter_number')
            #     .order_by('-chapter_number').values('chapter_number')[:1],
            #     output_field=models.IntegerField()
            # )
        )

        return queryset
