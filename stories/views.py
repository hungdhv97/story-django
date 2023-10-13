from django_filters import rest_framework as filters
from rest_framework.views import APIView

from .models import Story
from .pagination import CustomPagination
from .serializers import StorySerializer


class StoryFilter(filters.FilterSet):
    authorId = filters.NumberFilter(field_name="author_id")
    genreId = filters.NumberFilter(method='filter_by_genre')
    slug = filters.CharFilter(field_name="slug")
    isHot = filters.BooleanFilter(field_name="is_hot")
    isNew = filters.BooleanFilter(field_name="is_new")
    isCompleted = filters.BooleanFilter(field_name="status", method='filter_by_status')

    class Meta:
        model = Story
        fields = []

    def filter_by_genre(self, queryset, name, value):
        return queryset.filter(genres__id=value)

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=Story.Status.COMPLETED if value else Story.Status.ONGOING)


class StoryListView(APIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        stories = Story.objects.all()
        filt = StoryFilter(request.GET, queryset=stories)
        paginated_stories = self.pagination_class().paginate_queryset(filt.qs, request)
        serializer = self.serializer_class(paginated_stories, many=True)
        return self.pagination_class().get_paginated_response(serializer.data)
