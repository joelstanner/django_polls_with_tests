"""Polls application for django tutorial."""
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    """Index page."""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Return a detail view based on question_id."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """Return a results view based on question_id."""
    response = "You're looking at the results of question {}."
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    """Return a vote view based on question_id."""
    return HttpResponse("You're voting on question {}.".format(question_id))
