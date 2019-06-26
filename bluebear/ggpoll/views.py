from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import GGQuestion, GGAnswer


def index(request):
    questions = GGQuestion.objects.all()
    template = loader.get_template("bbpoll/index.html")
    context = {"questions": questions}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = GGQuestion.objects.get(pk=question_id)
    except GGQuestion.DoesNotExist:
        raise Http404("GGQuestion not found, Bluebear is sad :(")
    return render(request, "bbpoll/detail.html", {"question":question})

def results(request, question_id):
    question = get_object_or_404(GGQuestion, pk=question_id)
    return render(request, "bbpoll/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(GGQuestion, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, GGAnswer.DoesNotExist):
        return render(request, "bbpoll/detail.html", {"question":question, "error_message": "You didn't select a choice please select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("bbpoll:results", args=(question.id,)))
