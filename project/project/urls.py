from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from polls import views


router = DefaultRouter()
# router.register(r'polls', views.PoolViewSet)
router.register(r'polls', views.PoolNestedViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(router.urls)),
]
