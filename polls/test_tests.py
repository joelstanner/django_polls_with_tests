"""Tests for django polls tutorial app."""
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Question

import datetime


def create_question(question_text, days):
    """Create a question.

    Using the given `question_text` and published the
    given number of `days` offset to now (negative for questions publised
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


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
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "test 1")

    def test_index_no_questions(self):
        """If no polls are available, display appropriate message."""
        self.question1.delete()
        self.question2.delete()
        response = self.client.get(reverse('polls:index'))
        assert response.status_code == 200
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_with_old_question(self):
        """Questions with past dates should be visible."""
        create_question(question_text="Past Question.", days=-30)
        self.question1.delete()
        self.question2.delete()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question.>'])

    def test_index_with_only_future_question(self):
        """Future questions should not appear on index page."""
        create_question(question_text="Future Question.", days=30)
        self.question1.delete()
        self.question2.delete()
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

# Detail Tests

    def test_detail_view(self):
        response = self.client.get('/polls/1/')
        self.assertContains(response, "test 1")
        self.assertTemplateUsed(response, 'polls/detail.html')

# Results View

    def test_results_view(self):
        response = self.client.get('/polls/1/results/')
        self.assertContains(response, "test 1")
        self.assertContains(response, "test1 choice2")
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
        """Does the published recently filter work with current and old q's?"""
        from polls.models import Question
        q = Question(question_text="test 1", pub_date=timezone.now())
        q2 = Question(question_text="test 2",
                      pub_date=timezone.now() - datetime.timedelta(days=2))

        assert q.was_published_recently() is True
        assert q2.was_published_recently() is False

    def test_was_published_recently_with_future_q(self):
        """Should return false for future questions."""
        from polls.models import Question
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        assert future_question.was_published_recently() is False

    def test_str_of_question(self):
        from polls.models import Question
        q = Question(question_text="test 1", pub_date=timezone.now())
        resp = str(q)
        assert resp == "test 1"

    def test_str_of_choice(self):
        from polls.models import Choice
        c = Choice(choice_text="choice 1")
        assert str(c) == "choice 1"
