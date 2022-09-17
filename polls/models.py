"""Model for Polls app."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model for polls app."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date to be ended', null=True, blank=True)

    def __str__(self):
        """Return string of question's text."""
        return self.question_text

    def was_published_recently(self):
        """Check if the question was published recently.

        :return: True if it is published recently else False
        """
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check if the question was published.

        :return: True if it pass the publish date, False if not
        """
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """Check if the question is still accepting vote.

        :return: True if it still in the voting period and False if not
        """
        now = timezone.localtime()
        if self.end_date is None:
            return self.is_published()
        return self.end_date >= now >= self.pub_date


class Choice(models.Model):
    """Choice model for polls app."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """count the number of votes for this choice."""
        count = Vote.objects.filter(choice=self).count()
        return count

    def __str__(self):
        """Return string for the choices."""
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        return self.question
