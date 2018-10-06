from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    questions = Question.objects.all()
    template = loader.get_template("bbpoll/index.html")
    context = {"questions": questions}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question not found, Bluebear is sad :(")
    return render(request, "bbpoll/detail.html", {"question":question})

def results(request, question_id):
    return HttpResponse("You're looking at the results of question {}.".format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
