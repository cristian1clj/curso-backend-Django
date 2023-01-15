from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name: str = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """
        Return the last five published questions
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name: str = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes amy question that arent published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())    


class ResultView(generic.DetailView):
    model = Question
    template_name: str = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices_list = question.choice_set.all()
    
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question, 
            'choices_list': choices_list, 
            'error_message': "No elegiste una respuesta"
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes +=  1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))