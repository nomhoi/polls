from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Pool, Question
from .serializers import PoolSerializer, QuestionSerializer


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
