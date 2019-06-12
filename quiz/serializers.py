# -*- coding: utf-8 -*-

from rest_framework import serializers as s


class QuestionProperties(s.Serializer):
    id = s.IntegerField(required=False)
    question_text = s.CharField(required=False)
    pub_date = s.DateTimeField(required=False)


class QuestionList(s.Serializer):
    id = s.IntegerField(required=False)
    question_text = s.CharField(required=False)


class QuestionForm(s.Serializer):
    question_text = s.CharField()
