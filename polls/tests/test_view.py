"""Test for Poll's View."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Question


def create_question(question_text, days, end_day=None):
    """Create a question using the give parameter.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    if end_day is None:
        return Question.objects.create(
            question_text=question_text, pub_date=time)
    end_day = timezone.now() + datetime.timedelta(days=end_day)
    return Question.objects.create(
        question_text=question_text, pub_date=time, end_date=end_day)


class QuestionIndexViewTests(TestCase):
    """Test for index page."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Test questions with a pub_date in the past."""
        question = create_question(question_text="Past question.",
                                   days=-30,
                                   end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """Test questions with a pub_date in the future."""
        create_question(question_text="Future question.",
                        days=30,
                        end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Test if both past and future questions exist.

        Test if both past and future questions exist
        but only past questions are displayed
        """
        question = create_question(question_text="Past question.",
                                   days=-30,
                                   end_day=15)
        create_question(question_text="Future question.",
                        days=30,
                        end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.",
                                    days=-30,
                                    end_day=15)
        question2 = create_question(question_text="Past question 2.",
                                    days=-5,
                                    end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
