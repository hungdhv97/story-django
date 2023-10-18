from django.urls import path

from .views import StoryListView, StoryDetailView

urlpatterns = [
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='story-detail'),
]
