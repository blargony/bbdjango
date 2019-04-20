from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question

class QuestionTests(TestCase):
    def test_was_published_recently(self):
        """
        was_published_recently() tests for futrue dates if they are future
        it will be false
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_time = Question(pub_date=time)
        self.assertEqual(future_time.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)


