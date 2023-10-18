from django.db.models import Count, Sum, Case, When, Value, BooleanField, Avg
from django.db.models.functions import Now, Round
from django.utils import timezone
from rest_framework.generics import ListAPIView

from .models import Story
from story_site.pagination import CustomPagination
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
                When(created_date__gte=Now() - timezone.timedelta(days=30), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            is_hot=Case(
                When(total_reads__gte=500, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            avg_rating=Round(Avg('rating__rating_value'), 2),
        )

        return queryset
