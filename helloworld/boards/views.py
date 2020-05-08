from django.shortcuts import render
from django.http import HttpResponse
from .models import Board, Topic, Post
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board=board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                creates_by=request.user
            )

            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
        else:
            form = NewTopicForm()
        return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board_pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})