from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Pagina principal de premios platzi app")


def detail(request, question_id):
    return HttpResponse(f"Pregunta #{question_id}")


def results(request, question_id):
    return HttpResponse(f"Resultados de la pregunta #{question_id}")


def vote(request, question_id):
    return HttpResponse(f"Votando en la pregunta #{question_id}")