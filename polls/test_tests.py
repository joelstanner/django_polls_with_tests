"""Tests for django polls tutorial app."""
from django.test import TestCase
from django.test import Client
from django.utils import timezone
import datetime


class PollsViewsTest(TestCase):
    """Define the various view tests for the polls app."""

    def setUp(self):
        from polls.models import Question
        Question.objects.create(question_text="test 1", pub_date=timezone.now())
        Question.objects.create(question_text="test 2", pub_date=timezone.now())
        self.client = Client()

    def test_index_view_correct(self):
        response = self.client.get('/polls/')
        assert response.content.decode() == "Hello, world. You're at the polls index."  # NOQA

    def test_detail_view(self):
        response = self.client.get('/polls/1/')
        assert response.content.decode() == "You're looking at question 1."

    def test_results_view(self):
        response = self.client.get('/polls/1/results/')
        expected = "You're looking at the results of question 1."
        assert response.content.decode() == expected

    def test_vote_view(self):
        response = self.client.get('/polls/1/vote/')
        assert response.content.decode() == "You're voting on question 1."


class PollsModelTest(TestCase):

    def test_was_published_recently(self):
        from polls.models import Question
        q = Question(question_text="test 1", pub_date=timezone.now())
        q2 = Question(question_text="test 2",
                      pub_date=timezone.now() - datetime.timedelta(days=2))

        assert q.was_published_recently() is True
        assert q2.was_published_recently() is False

    def test_str_of_question(self):
        from polls.models import Question
        q = Question(question_text="test 1", pub_date=timezone.now())
        resp = str(q)
        assert resp == "test 1"

    def test_str_of_choice(self):
        from polls.models import Choice
        c = Choice(choice_text="choice 1")
        assert str(c) == "choice 1"
