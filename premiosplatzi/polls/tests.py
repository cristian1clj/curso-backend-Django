import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recently_questions(self):
        """was_published_recently returns True for questions whose pub_date is less than 24 hours compared with the present date"""
        time = timezone.now() - datetime.timedelta(hours=12)
        present_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        
        self.assertIs(present_question.was_published_recently(), True)
        
    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for questions whose pub_date is more than 24 hours compared with the present date"""
        time = timezone.now() - datetime.timedelta(days=3, hours=2)
        past_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        
        self.assertIs(past_question.was_published_recently(), False)