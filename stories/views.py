from rest_framework.generics import ListAPIView

from .models import Story
from .pagination import CustomPagination
from .serializers import StorySerializer


class StoryListView(ListAPIView):
    serializer_class = StorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Story.objects.all()

        # Filter by author ID
        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            queryset = queryset.filter(author__id=author_id)

        # Filter by genre ID
        genre_id = self.request.query_params.get('genre_id', None)
        if genre_id is not None:
            queryset = queryset.filter(storygenre__genre__id=genre_id)

        # Filter by slug
        slug = self.request.query_params.get('slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        # Filter by isHot
        is_hot = self.request.query_params.get('is_hot', None)
        if is_hot is not None:
            is_hot = is_hot.lower() == 'true'
            # Assuming you have a method to determine if a story is hot
            queryset = queryset.filter(is_hot=is_hot)

        # Filter by isNew
        is_new = self.request.query_params.get('is_new', None)
        if is_new is not None:
            is_new = is_new.lower() == 'true'
            # Assuming you have a method to determine if a story is new
            queryset = queryset.filter(is_new=is_new)

        # Filter by isCompleted
        is_completed = self.request.query_params.get('is_completed', None)
        if is_completed is not None:
            is_completed = is_completed.lower() == 'true'
            status = 'completed' if is_completed else 'ongoing'
            queryset = queryset.filter(status=status)

        return queryset
