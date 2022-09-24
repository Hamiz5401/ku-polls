"""Test for authentication."""
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from ..models import Question, Vote


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


class AuthTest(TestCase):
    """Test cases for authentication."""

    def setUp(self):
        """Initialize the user data."""
        self.username = "tester"
        self.password = "123"
        self.user = User.objects.create_user(
                    username=self.username,
                    password=self.password,
                    email="tester@test.com"
        )
        self.user.save()

    def test_login_auth(self):
        """Check if the user can login properly."""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        login_data = {'username': self.username, 'password': self.password}
        # login with the data
        response = self.client.post(url, login_data)
        self.assertEqual(302, response.status_code)  # redirected
        # should redirect to the index page
        self.assertRedirects(response,
                             reverse('polls:index'))

    def test_auth_user_vote(self):
        """User that unauthenticated will be redirected to login page."""
        self.client.login(username=self.username, password=self.password)
        question = create_question("auth_check", days=-1)
        response = self.client.post(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(200, response.status_code)
        self.client.logout()
        response = self.client.post(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(302, response.status_code)

    def test_one_user_vote(self):
        """Each user should only have one vote."""
        self.client.login(username=self.username, password=self.password)
        question = create_question("auth_check", days=-1)
        choice1 = question.choice_set.create(choice_text='test1')
        choice2 = question.choice_set.create(choice_text='test2')
        self.client.post(reverse('polls:vote',
                                 args=(question.id,)),
                         {'choice': choice1.id})
        self.client.post(reverse('polls:vote',
                                 args=(question.id,)),
                         {'choice': choice2.id})
        self.assertEqual(Vote.objects.count(), 1)
