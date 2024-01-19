from django.urls import path

from .views import StoryListView, StoryDetailView, ChapterListView, ChapterDetailView, RatingCreateView, GenreListView, \
    StorySearchView, ChapterShortInfoListView, TopStoryListView

urlpatterns = [
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<slug:slug>/chapters/', ChapterListView.as_view(), name='chapter-list'),
    path('top/stories/', TopStoryListView.as_view(), name='top-story-list'),
    path('stories/<slug:slug>/chapters/short-info/', ChapterShortInfoListView.as_view(),
         name='chapter-short-info-list'),
    path('chapters/<int:chapterId>/', ChapterDetailView.as_view(), name='chapter-detail'),
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('search/', StorySearchView.as_view(), name='story-search'),
]
