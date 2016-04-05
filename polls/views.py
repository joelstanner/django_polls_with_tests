"""Polls application for django tutorial."""
from django.http import HttpResponse


def index(request):
    """Index page."""
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    """Return a detail view based on question_id."""
    return HttpResponse("You're looking at question {}.".format(question_id))


def results(request, question_id):
    """Return a results view based on question_id."""
    response = "You're looking at the results of question {}."
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    """Return a vote view based on question_id."""
    return HttpResponse("You're voting on question {}.".format(question_id))
