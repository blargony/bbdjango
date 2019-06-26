import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils import timezone


class GGQuestion(models.Model):
    """
    GG Question.  The text of one question asked.
    Includes an option to make the question active or hide it
    while we finish work on the answers.
    """
    question_text = models.CharField(max_length=200)
    active = models.BooleanField()

    def __str__(self):
        return self.question_text


class GGAnswer(models.Model):
    """
    Possible answer to a given question.
    Includes the weighting for which God the user favors.
    """
    question = models.ForeignKey(GGQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    jupiter = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.choice_text


class GGUser(models.Model):
    """
    A user taking the poll.  Holds the log of the answers they have given.

    Allows the user to create a name and personal motto for fun.
    """
    name = models.CharField(max_length=100)
    motto = models.CharField(max_length=300)

    answers = models.ManyToManyField(GGAnswer)

    def __str__(self):
        return self.name
