import json
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Choice, Poll, Question, UserResponse
from .serializers import PollNestedQuestionSerializer, PollNestedUserResponseSerializer, PollSerializer


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


class PollNestedViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Poll.objects.all().prefetch_related('questions__choices')
    serializer_class = PollNestedQuestionSerializer
    permission_classes = [AllowAny]
    permission_classes_by_action = {
        'create':     [IsAdminUser],
        'retrieve':   [IsAuthenticated],
        'destroy':    [IsAdminUser],
        'update':     [IsAdminUser],
    }

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
                values('id', 'choice__id', 'boolean_response', 'text_response')

            user_responses = {ur['choice__id']: ur for ur in ur_objects}

            for question in data['questions']:
                for choice in question['choices']:
                    choice_id = choice['id']
                    if choice_id in user_responses:
                        choice['respond_id'] = user_responses[choice_id]['id']
                        if user_responses[choice_id]['boolean_response']:
                            choice['respond'] = user_responses[choice_id]['boolean_response']
                        else:
                            choice['respond'] = user_responses[choice_id]['text_response']
                    else:
                        if question['type'] == 1:
                            choice['respond'] = ''
                        else:    
                            choice['respond'] = False                            

        return Response(data)


class PollNestedUserResponseViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления ответов.
    """
    queryset = Poll.objects.all()
    serializer_class = PollNestedUserResponseSerializer
    permission_classes = [IsAuthenticated]
