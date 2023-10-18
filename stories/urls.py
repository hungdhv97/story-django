from django.urls import path

from .views import StoryListView, StoryDetailView, ChapterListView, ChapterDetailView, RatingCreateView, GenreListView, \
    StorySearchView

urlpatterns = [
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<slug:slug>/chapters/', ChapterListView.as_view(), name='chapter-list'),
    path('chapters/<int:chapterId>/', ChapterDetailView.as_view(), name='chapter-detail'),
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('search/', StorySearchView.as_view(), name='story-search'),

]
