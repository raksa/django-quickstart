import pytest
import json
import pytz
from quiz import serializers as s
from django.test import RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken import models as am
from rest_framework.renderers import JSONRenderer

from quiz import models as m
from quiz import views as v

from datetime import datetime


def get_response_json(response):
    response.render()
    return json.loads(response.content.decode('utf-8'))


def serializer_data_to_json(serializer):
    b_json = JSONRenderer().render(serializer.data)
    return json.loads(b_json.decode('utf-8'))


def fixture_user(num_zones=0, idx=1):
    user = User.objects.create_user(
        username='testuser{}'.format(idx), email=None, password='secret')
    token = am.Token.objects.create(user=user)
    return user, token


@pytest.fixture
def user1():
    return fixture_user()[0]


@pytest.fixture
def q1():
    q = m.Question.objects.create(
        question_text='What is your name', pub_date=datetime(2020, 1, 1, tzinfo=pytz.utc))

    c1 = m.Choice.objects.create(choice_text='Andy', votes=1, question=q)
    c2 = m.Choice.objects.create(choice_text='Nant', votes=1, question=q)
    return q


#########################################################
# QuestionList
#########################################################


class TestQuestionList(object):
    @pytest.mark.django_db
    def test_get_question_list_should_return_list_of_questions(self, q1):
        user, token = fixture_user()
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        questions_data = serializer_data_to_json(
            s.QuestionList([q1], many=True))

        factory = RequestFactory()
        request = factory.get('/questions', **headers)
        response = v.QuestionList.as_view()(request)
        assert response.status_code == 200
        assert get_response_json(response) == questions_data

        client = Client()
        response = client.get('/v1/questions', **headers)
        assert response.status_code == 200
        assert get_response_json(response) == questions_data

    @pytest.mark.django_db
    def test_get_question_list_should_return_401_unauthorized(self):
        factory = RequestFactory()
        request = factory.get('/questions')
        response = v.QuestionList.as_view()(request)
        assert response.status_code == 401

        client = Client()
        response = client.get('/v1/questions')
        assert response.status_code == 401
