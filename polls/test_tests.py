"""Tests for django polls tutorial app."""
from django.test import TestCase
from django.utils import timezone
import datetime


class PollsViewsTest(TestCase):
    """Define the various view tests for the polls app."""

    def setUp(self):
        from polls.models import Question
        self.question1 = Question.objects.create(question_text="test 1",
                                                 pub_date=timezone.now())
        self.question2 = Question.objects.create(question_text="test 2",
                                                 pub_date=timezone.now())
        self.choice1 = self.question1.choice_set.create(
            choice_text="test1 choice1"
        )
        self.choice2 = self.question1.choice_set.create(
            choice_text="test1 choice2"
        )

# Index Tests

    def test_index_view_correct(self):
        response = self.client.get('/polls/')
        self.assertContains(response, "test 1")

# Detail Tests

    def test_detail_view(self):
        response = self.client.get('/polls/1/')
        self.assertContains(response, "test 1")
        self.assertTemplateUsed(response, 'polls/detail.html')

# Results View

    def test_results_view(self):
        response = self.client.get('/polls/1/results/')
        self.assertContains(response, "test 1")
        self.assertContains(response, "test 2")
        self.assertTemplateUsed(response, 'polls/results.html')

# Vote Tests

    def test_vote_view(self):
        response = self.client.get('/polls/1/vote/')
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_vote_posts(self):
        response = self.client.post('/polls/1/vote/',
                                    {'choice': 1},
                                    follow=True)
        vote_count = self.question1.choice_set.first().votes
        assert vote_count == 1
        self.assertRedirects(response, '/polls/1/results/')

    def test_vote_post_error_correct(self):
        response = self.client.post('/polls/1/vote/',
                                    {'choice': '3'},
                                    follow=True)
        assert response.context['error_message'] == 'Select a valid choice.'
        self.assertTemplateUsed(response, 'polls/detail.html')


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
