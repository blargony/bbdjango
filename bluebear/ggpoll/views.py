from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from collections import defaultdict

from .models import GGQuestion, GGAnswer, GGUser


def index(request):
    """Show welcome to the sorting quiz."""
    template = loader.get_template("ggpoll/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def begin(request):
    """Create a simple user that we link all the answers to."""
    request.session.flush()  # "Logout" from any previous session

    try:
        new_name = request.POST["name"]
        new_motto = request.POST["motto"]
    except KeyError:
        if request.method == "GET":
            context = {}
        else:
            context = {"error_message": "Please pick a name and motto for yourself!"}
        return render(request, "ggpoll/begin.html", context)
    else:
        # Create the new user and store the user info into the Session
        # then redirect to the first question
        new_user = GGUser(name=new_name, motto=new_motto)
        new_user.save()
        request.session['user_id'] = new_user.id  # 'log in' with new user
        first_question = GGQuestion.objects.all()[0]
        return HttpResponseRedirect(reverse("ggpoll:ask_question", args=(first_question.id, )))


def ask_question(request, question_id):
    question = get_object_or_404(GGQuestion, pk=question_id)
    answers = get_object_or_404(GGAnswer, pk=question_id)
    try:
        selected_answer = question.gganswer_set.get(pk=request.POST["answer"])
    except (KeyError, GGAnswer.DoesNotExist):
        return render(request, "ggpoll/ask.html",
                      {"question": question,
                       "answers": answers,
                       "error_message": "You didn't select an answer!"})
    else:
        user = get_object_or_404(GGUser, pk=request.session['user_id'])
        user.answers.add(selected_answer)
        user.save()
        try:
            next_question = GGQuestion.objects.get(pk=question_id+1)
            return HttpResponseRedirect(reverse("ggpoll:ask_question", args=(next_question.id,)))
        except GGQuestion.DoesNotExist:
            return HttpResponseRedirect(reverse("ggpoll:results"))



def results(request):
    user = get_object_or_404(GGUser, pk=request.session['user_id'])
    totals = defaultdict(int)
    for answer in user.answers.all():
        for weighted_group in answer.gggroupweight_set.all():
            totals[weighted_group.group] += weighted_group.weight
    sorted_totals = sorted(totals, key=totals.get)
    context = {"top_score": sorted_totals[0]}
    return render(request, "ggpoll/results.html", context)


