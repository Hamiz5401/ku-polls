"""View for Polls app."""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Question, Choice, Vote


def showtime(request) -> HttpResponse:
    """Return the local time and date."""
    thaitime = timezone.localtime()
    msg = f"<p>The time is {thaitime}.</p>"
    return HttpResponse(msg)


class IndexView(generic.ListView):
    """Index page that display the latest 5 questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.

        :return: last five published question
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail page for each questions."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def dispatch(self, request, *args, **kwargs):
        """Redirect user to index page when voting is not allow."""
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll")
            return redirect(reverse('polls:index'))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add more context to the template of this page."""
        context = super().get_context_data(**kwargs)
        question = Question.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        if user.is_authenticated:
            try:
                existed_vote = Vote.objects.get(user=user, choice__in=question.choice_set.all()).choice.choice_text
                context['existed_vote'] = existed_vote
            except Vote.DoesNotExist:
                pass
        return context


class ResultsView(generic.DetailView):
    """Result page for each questions."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Function that accept vote(s) from detail page."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            user_vote = Vote.objects.get(user=request.user, choice__question=question)
            user_vote.choice = selected_choice
            user_vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(choice=selected_choice, user=request.user)
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
