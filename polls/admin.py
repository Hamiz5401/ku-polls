"""Admin page for Polls app."""
from django.contrib import admin

from .models import Question

admin.site.register(Question)
