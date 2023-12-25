import subprocess

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ListStoriesCrawlForm, SomeStoriesCrawlForm


def crawl_list_stories_view(request):
    if request.method == 'POST':
        form = ListStoriesCrawlForm(request.POST)
        if form.is_valid():
            from_story_index = form.cleaned_data['from_story_index']
            to_story_index = form.cleaned_data['to_story_index']
            from_chapter_index = form.cleaned_data['from_chapter_index']
            to_chapter_index = form.cleaned_data['to_chapter_index']

            try:
                # Prepare the management command with its arguments
                command = [
                    'python', 'manage.py', 'crawl_list_stories',
                    '--from-story-index', str(from_story_index),
                    '--to-story-index', str(to_story_index),
                    '--from-chapter-index', str(from_chapter_index),
                    '--to-chapter-index', str(to_chapter_index)
                ]

                # Run the command asynchronously
                subprocess.Popen(command)

                messages.success(request, 'Stories crawl initiated successfully.')
            except Exception as e:
                messages.error(request, f'Error occurred: {e}')

            # Redirect to the same page or another success page
            return redirect('crawl-list-stories')
    else:
        form = ListStoriesCrawlForm()

    return render(request, 'crawl_list_stories.html', {'form': form})


def crawl_some_stories_view(request):
    if request.method == 'POST':
        form = SomeStoriesCrawlForm(request.POST)
        if form.is_valid():
            story_urls = form.cleaned_data['story_urls']
            from_chapter_index = form.cleaned_data['from_chapter_index']
            to_chapter_index = form.cleaned_data['to_chapter_index']

            try:
                command = [
                    'python', 'manage.py', 'crawl_some_stories',
                    '--story-urls', story_urls,
                    '--from-chapter-index', str(from_chapter_index),
                    '--to-chapter-index', str(to_chapter_index)
                ]
                subprocess.Popen(command)
                messages.success(request, 'Story crawling initiated successfully.')
            except Exception as e:
                messages.error(request, f'Error occurred: {e}')

            return redirect('crawl-some-stories')
    else:
        form = SomeStoriesCrawlForm()

    return render(request, 'crawl_some_stories.html', {'form': form})
