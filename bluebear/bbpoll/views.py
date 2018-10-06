from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    questions = Question.objects.all()
    template = loader.get_template("bbpoll/index.html")
    context = {"questions": questions}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question {}.".format(question_id))

def results(request, question_id):
    return HttpResponse("You're looking at the results of question {}.".format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
