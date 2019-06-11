# -*- coding: utf-8 -*-

import pytest
import json
from doorman import serializers as s
from django.test import RequestFactory
from django.test import Client
from rest_framework.authtoken import models as am
from rest_framework.renderers import JSONRenderer

from core import models as m
from doorman import views as v


def get_response_json(response):
    response.render()
    return json.loads(response.content.decode('utf-8'))


def serializer_data_to_json(serializer):
    b_json = JSONRenderer().render(serializer.data)
    return json.loads(b_json.decode('utf-8'))


def fixture_user(num_zones=0, idx=1):
    user = m.User.objects.create_user(
        username='testuser{}'.format(idx), email=None, password='secret')
    token = am.Token.objects.create(user=user)
    return user, token


@pytest.fixture
def user1():
    return fixture_user()[0]


#########################################################
# QuestionList
#########################################################


class TestQuestionList(object):
    @pytest.mark.django_db
    def test_get_question_list_should_return_list_of_questions(self):
        user, token, _ = fixture_user()
        user_data = serializer_data_to_json(s.User(user))
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        factory = RequestFactory()
        request = factory.get('/questions', **headers)
        response = v.UserProfile.as_view()(request)
        assert response.status_code == 200
        assert get_response_json(response) == user_data

        client = Client()
        response = client.get('/v1/questions', **headers)
        assert response.status_code == 200
        assert get_response_json(response) == user_data

    @pytest.mark.django_db
    def test_get_question_list_should_return_401_unauthorized(self):
        factory = RequestFactory()
        request = factory.get('/questions')
        response = v.UserProfile.as_view()(request)
        assert response.status_code == 401

        client = Client()
        response = client.get('/v1/questions')
        assert response.status_code == 401
