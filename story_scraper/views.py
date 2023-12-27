import subprocess

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from .forms import ListStoriesCrawlForm, SomeStoriesCrawlForm


@staff_member_required
def crawl_list_stories_view(request):
    command = ''
    form = ListStoriesCrawlForm()
    if request.method == 'POST':
        form = ListStoriesCrawlForm(request.POST)
        if form.is_valid():
            from_story_index = form.cleaned_data['from_story_index']
            to_story_index = form.cleaned_data['to_story_index']
            from_chapter_index = form.cleaned_data['from_chapter_index']
            to_chapter_index = form.cleaned_data['to_chapter_index']

            command = f'python manage.py crawl_list_stories --from-story-index {from_story_index} --to-story-index {to_story_index} --from-chapter-index {from_chapter_index} --to-chapter-index {to_chapter_index}'
            messages.info(request, 'Command prepared for execution. Please check the output below.')
    context = {
        'form': form,
        'command': command,
    }
    return render(request, 'crawl_stories.html', context)


@staff_member_required
def crawl_some_stories_view(request):
    command = ''
    form = SomeStoriesCrawlForm()
    if request.method == 'POST':
        form = SomeStoriesCrawlForm(request.POST)
        if form.is_valid():
            story_urls = form.cleaned_data['story_urls']
            from_chapter_index = form.cleaned_data['from_chapter_index']
            to_chapter_index = form.cleaned_data['to_chapter_index']

            command = f"python manage.py crawl_some_stories --story-urls {story_urls} --from-chapter-index {from_chapter_index} --to-chapter-index {to_chapter_index}"
            messages.info(request, 'Story crawling completed successfully.')
    context = {
        'form': form,
        'command': command
    }
    return render(request, 'crawl_stories.html', context)
