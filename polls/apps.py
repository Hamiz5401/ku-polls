"""Application for Polls app."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls config app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
