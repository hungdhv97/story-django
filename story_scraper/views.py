import subprocess

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import StoryCrawlForm


def crawl_stories_view(request):
    if request.method == 'POST':
        form = StoryCrawlForm(request.POST)
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
            return redirect('crawl-stories')
    else:
        form = StoryCrawlForm()

    return render(request, 'crawl_stories.html', {'form': form})
