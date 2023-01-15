import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days=0, hours=0):
    """
    Create an question object, taking the 'question_text', 'days', and 'hours'.
    The days and the hours are added to the actual date. Positive days for future question, 
    negative days for past question, and 0 days for questions posted now. Its the same for hours.
    """
    time = timezone.now() + datetime.timedelta(days=days, hours=hours)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the future
        """
        future_question = create_question("¿Quien es el mejor CD de Platzi?", days=30)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recently_questions(self):
        """
        was_published_recently returns True for questions whose pub_date is less than 24 hours 
        compared with the present date
        """
        present_question = create_question("¿Quien es el mejor CD de Platzi?", hours=-12)
        self.assertIs(present_question.was_published_recently(), True)
        
    def test_was_published_recently_with_past_question(self):
        """
        was_published_recently returns False for questions whose pub_date is more than 24 hours 
        compared with the present date
        """
        past_question = create_question("¿Quien es el mejor CD de Platzi?", days=-3, hours=-2)
        self.assertIs(past_question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """
        If no question exist, an appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avaiable")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
    def test_future_questions(self):
        """
        If a future question is stored, it cant be displayed
        """
        future_question = create_question("¿Quien es el mejor CD de Platzi?", days=12)
        future_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are avaiable")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
    def test_past_questions(self):
        """
        If a past question is stored, it will be displayed
        """
        past_question = create_question("¿Quien es el mejor CD de Platzi?", days=-12)
        past_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])
        
    def test_past_and_future_questions(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        past_question = create_question("¿Quien es el mejor CD de Platzi?", days=-23)
        past_question.save()
        future_question = create_question("¿Quien es el peor CD de Platzi?", days=30)
        future_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_multiple_past_question(self):
        """
        If there are multiple past questions stored, they will be displayed.
        """
        past_question1 = create_question("¿Quien es el mejor CD de Platzi?", days=-23)
        past_question1.save()
        past_question2 = create_question("¿Quien es el peor CD de Platzi?", days=-24)
        past_question2.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])
    
    def test_multiple_future_question(self):
        """
        If there are multiple future questions, they will not be displayed.
        """
        future_question1 = create_question("¿Quien es el mejor CD de Platzi?", days=23)
        future_question1.save()
        future_question2 = create_question("¿Quien es el peor CD de Platzi?", days=24)
        future_question2.save()
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are avaiable")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])