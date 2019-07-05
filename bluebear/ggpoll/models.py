from django.db import models


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

    class Meta:
        verbose_name = 'Poll Question'


class GGGroup(models.Model):
    """A group that a User can be a member of."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'God'


class GGAnswer(models.Model):
    """
    Possible answer to a given question.
    Then links to the groups (e.g. Gods, Houses, etc.) that this
    answer will associate the user with.   The link to the groups includes
    a programmable weighting, so the answer can be loosely or strongly
    coorelated with a given grouping.
    """
    question = models.ForeignKey(GGQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    groups = models.ManyToManyField(GGGroup, through='GGGroupWeight')

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Answer'


class GGGroupWeight(models.Model):
    WEIGHT_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3)
    )
    group = models.ForeignKey(GGGroup, on_delete=models.CASCADE)
    answer = models.ForeignKey(GGAnswer, on_delete=models.CASCADE)
    weight = models.IntegerField(choices=WEIGHT_CHOICES, default=3)


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

    class Meta:
        verbose_name = 'Poll User'
