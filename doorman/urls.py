# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'questions/?$', views.QuestionList.as_view()),
    url(r'questions/(?P<q_id>[0-9]+)/?$', views.QuestionProperties.as_view()),
]
