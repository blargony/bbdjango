from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    questions = Question.objects.all()
    output = ""
    for q in questions:
        output += q.question_text
        output += "\n"
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("You're looking at question {}.".format(question_id))

def results(request, question_id):
    return HttpResponse("You're looking at the results of question {}.".format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
