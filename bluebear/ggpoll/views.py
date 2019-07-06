"""Our Views."""
from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import GGQuestion, GGAnswer, GGUser


def index(request):
    """Show welcome to the sorting quiz."""
    template = loader.get_template("ggpoll/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def begin(request):
    """Create a simple user that we link all the answers to."""
    request.session.flush()  # "Logout" from any previous session

    if request.method == "POST":
        new_name = request.POST["name"]
        new_motto = request.POST["motto"]
        # Try this again if they didn't put in a name
        if not new_name or not new_motto:
            context = {"error_message": "Please pick a name and motto for yourself!"}
            return render(request, "ggpoll/begin.html", context)
        # Create the new user and store the user info into the Session
        # then redirect to the first question
        new_user = GGUser(name=new_name, motto=new_motto)
        new_user.save()
        request.session['user_id'] = new_user.id  # 'log in' with new user
        first_question = GGQuestion.objects.all()[0]
        return HttpResponseRedirect(reverse("ggpoll:ask_question", args=(first_question.id, )))
    return render(request, "ggpoll/begin.html")


def ask_question(request, question_id):
    """Get and Post view for working through the list of questions."""
    question = get_object_or_404(GGQuestion, pk=question_id)
    answers = get_object_or_404(GGAnswer, pk=question_id)
    question_count = len(GGQuestion.objects.all())
    try:
        selected_answer = question.gganswer_set.get(pk=request.POST["answer"])
    except (KeyError, GGAnswer.DoesNotExist):
        context = {
            "question": question,
            "question_count": question_count,
            "answers": answers,
        }
        if request.method == "POST":
            context = {"error_message": "You didn't select an answer!"}
        return render(request, "ggpoll/ask_question.html", context)
    else:
        user = get_object_or_404(GGUser, pk=request.session['user_id'])
        user.answers.add(selected_answer)
        user.save()
        next_question = GGQuestion.objects.filter(
            active=True, pk__gt=question.pk).order_by('pk').first()
        if next_question:
            return HttpResponseRedirect(reverse("ggpoll:ask_question", args=(next_question.id,)))
        return HttpResponseRedirect(reverse("ggpoll:results"))


def results(request, user_id=None):
    """Add up the users scores and show the results."""
    if not user_id:
        user = get_object_or_404(GGUser, pk=request.session['user_id'])
    else:
        user = get_object_or_404(GGUser, pk=user_id)
    totals = defaultdict(int)
    for answer in user.answers.all():
        for weighted_group in answer.gggroupweight_set.all():
            totals[weighted_group.group] += weighted_group.weight
    sorted_totals = sorted(totals, key=totals.get)
    context = {
        "top_score": sorted_totals[-1],
        "totals": totals.items(),
        "user": user,
    }
    return render(request, "ggpoll/results.html", context)
