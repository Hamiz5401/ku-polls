from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class AuthTest(TestCase):

    def setUp(self):
        self.username = "tester"
        self.password = "123"
        self.user = User.objects.create_user(
                    username=self.username,
                    password=self.password,
                    email="tester@test.com"
        )
        self.user.save()

    def test_login_auth(self):
        """check if the user can login properly"""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        login_data = {'username': self.username, 'password': self.password}
        # login with the data
        response = self.client.post(url, login_data)
        self.assertEqual(302, response.status_code)  # redirected
        self.assertRedirects(response, reverse('polls:index'))  # should redirect to the index page
