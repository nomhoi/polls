from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from polls import views


router = DefaultRouter()
router.register(r'polls', views.PoolViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(router.urls)),
]
