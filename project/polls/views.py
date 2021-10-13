from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Pool
from .serializers import PoolSerializer

class PoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
    permission_classes_by_action = {
        'create':   [IsAdminUser],
        'destroy':  [IsAdminUser],
        'list':     [IsAuthenticatedOrReadOnly],
        'update':   [IsAdminUser],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            raise MethodNotAllowed(self.action)
            