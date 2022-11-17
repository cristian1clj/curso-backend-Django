from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.all()
    context = {
        'latest_question_list': latest_question_list
    }
    
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, id=question_id)
    choices_list = question.choice_set.all()
    
    context = {
        'question': question, 
        'choices_list': choices_list
    }
    
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    return HttpResponse(f"Resultados de la pregunta #{question_id}")


def vote(request, question_id):
    return HttpResponse(f"Votando en la pregunta #{question_id}")