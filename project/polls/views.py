from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Choice, Pool, Question
from .serializers import ChoiceSerializer, PoolSerializer, QuestionSerializer, PoolNestedSerializer


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


class PoolViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
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


class PoolNestedViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Pool.objects.all()
    serializer_class = PoolNestedSerializer
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
            serializer = PoolSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PoolSerializer(queryset, many=True)
        return Response(serializer.data)
        