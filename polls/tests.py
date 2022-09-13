"""Unit test for Polls app."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


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


class QuestionModeTests(TestCase):
    """test for Question model."""

    def test_was_published_recently_with_future_question(self):
        """Check if the question was published recently(with future question).

        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Check if the question was published recently(with old question).

        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Check if the question was published recently(with recent question).

        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    """Test for index page."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30, end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30, end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30, end_day=15)
        create_question(question_text="Future question.", days=30, end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30, end_day=15)
        question2 = create_question(question_text="Past question 2.", days=-5, end_day=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """Test for detail page."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 302 redirect."""
        future_question = create_question(question_text='Future question.', days=5, end_day=15)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5, end_day=15)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class Question_can_vote_and_is_published_test(TestCase):
    """Test for Question can_vote and is_published function."""

    def test_pubdate_in_future(self):
        """Test for question that pub_date is in the future.

        :return: False because future is not published and can't vote
        """
        future_question = create_question('Future question', days=5, end_day=15)
        self.assertFalse(future_question.is_published())
        self.assertFalse(future_question.can_vote())

    def test_pub_date_and_end_date_is_now(self):
        """Test for question that pub_date is now.

        :return: True when pub_date is now
        """
        question = create_question('Now', days=0)
        self.assertIs(True, question.is_published())
        self.assertIs(True, question.can_vote())

    def test_end_date_is_now(self):
        """Test for question that end_date is now.

        :return: True when end_date is now
        """
        question = create_question("end_now", days=-1, end_day=0.0000001)
        self.assertIs(True, question.is_published())
        self.assertIs(True, question.can_vote())

    def test_pass_end_date(self):
        """Test for question that pass the end_date.

        :return: False for can_vote when it pass the end_date but True for is_published
        """
        question = create_question("pass_end", days=-5, end_day=-1)
        self.assertIs(True, question.is_published())
        self.assertIs(False, question.can_vote())

    def test_end_date_null(self):
        """Test for question that end_date is null.

        :return: True when pub_date is now or have passed
        """
        question = create_question("end_date_is_null", days=0)
        self.assertIs(True, question.is_published())
        self.assertIs(True, question.can_vote())

    def test_question_within_poll_period(self):
        """Test for question that is still in the voting period.

        :return: True when The question is in the voting period
        """
        question = create_question("I can vote", days=-1, end_day=5)
        self.assertIs(True, question.is_published())
        self.assertIs(True, question.can_vote())
