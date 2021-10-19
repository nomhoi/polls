import json
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Choice, Poll, Question, UserResponse
from .serializers import ChoiceSerializer, PollSerializer, QuestionSerializer, PollNestedSerializer


class MixedPermissionModelViewSet(viewsets.ModelViewSet):
    """
    Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsAdminUser]}
    """

    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class PollViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [AllowAny]
    permission_classes_by_action = {
        'create':     [IsAdminUser],
        'destroy':     [IsAdminUser],
        'update':     [IsAdminUser],
    }


class QuestionViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления вопросов.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    permission_classes_by_action = {
        'create':     [IsAdminUser],
        'destroy':     [IsAdminUser],
        'update':     [IsAdminUser],
    }


class ChoiceViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления вариантов ответов
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]
    permission_classes_by_action = {
        'create':     [IsAdminUser],
        'destroy':     [IsAdminUser],
        'update':     [IsAdminUser],
    }


class PollNestedViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Poll.objects.all()
    serializer_class = PollNestedSerializer
    permission_classes = [AllowAny]
    permission_classes_by_action = {
        'create':     [IsAdminUser],
        'retrieve':   [IsAuthenticated],
        'destroy':    [IsAdminUser],
        'update':     [IsAdminUser],
    }

    def get_queryset(self):
        return Poll.objects.all().prefetch_related('questions__choices')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PollSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PollSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)        
        data = serializer.data

        if not request.user.is_staff:
            ur_objects = UserResponse.objects.filter(user=request.user, poll=instance). \
                values('choice__id', 'boolean_response', 'text_response')

            user_responses = {}
            for ur in ur_objects:
                if ur['boolean_response']:
                    user_responses[ur['choice__id']] = ur['boolean_response']
                else:
                    user_responses[ur['choice__id']] = ur['text_response']

            for question in data['questions']:
                for choice in question['choices']:
                    choice_id = choice['id']
                    if choice_id in user_responses:
                        choice['respond'] = user_responses[choice_id]
                    else:
                        if question['type'] == 1:
                            choice['respond'] = ''
                        else:    
                            choice['respond'] = False

        # print(json.dumps(data, indent=4))

        return Response(data)
