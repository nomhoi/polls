from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Pool
from .serializers import PoolSerializer

class PoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet для добавления, обновления и удаления опросов.
    """
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    