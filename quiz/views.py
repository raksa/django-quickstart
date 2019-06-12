from rest_framework import generics as rfg
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from . import permissions as pm
from . import serializers as s
from . import models as m

from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class QuestionList(rfg.ListCreateAPIView):
    """List of question"""
    queryset = ''
    permission_classes = (IsAuthenticated, pm.SuperAdmin)
    serializer_class = s.QuestionList

    @swagger_auto_schema(tags=['v1_question'])
    def get(self, request, *args, **kwargs):
        """Get list of questions"""
        questions = m.Question.objects.all()[:100]
        serializer = self.get_serializer_class()(questions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=s.QuestionForm, responses={'201': s.QuestionProperties}, tags=['v1_question'])
    def post(self, request, *args, **kwargs):
        """Create question"""
        question = m.Question.objects.all()[0]
        serializer = self.QuestionProperties(question)
        return Response(serializer.data, status=201)


class QuestionProperties(rfg.RetrieveUpdateDestroyAPIView):
    """Question's properties"""
    permission_classes = (IsAuthenticated, pm.SuperAdmin)
    serializer_class = s.QuestionProperties

    @swagger_auto_schema(tags=['v1_question'])
    def get(self, request, q_id, *args, **kwargs):
        """Retrieve question's properties"""
        question = get_object_or_404(m.Question, id=q_id)
        self.check_object_permissions(request, question)
        serializer = self.get_serializer_class()(question)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=s.QuestionForm, responses={'200': s.QuestionProperties}, tags=['v1_question'])
    def put(self, request, q_id, *args, **kwargs):
        """Update question properties"""
        question = get_object_or_404(m.Question, id=q_id)
        self.check_object_permissions(request, question)
        return self.get(request, q_id, *args, **kwargs)

    @swagger_auto_schema(request_body=s.QuestionForm, responses={'200': s.QuestionProperties}, tags=['v1_question'])
    def patch(self, request, q_id, *args, **kwargs):
        """Partial update question properties"""
        return self.put(request, q_id)

    @swagger_auto_schema(tags=['v1_question'])
    def delete(self, request, q_id, *args, **kwargs):
        """Delete question"""
        question = get_object_or_404(m.Question, id=q_id)
        self.check_object_permissions(request, question)
        return Response(204)
