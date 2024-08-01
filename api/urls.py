from django.urls import path,include
from rest_framework import routers
from api.views import StandardViewSet,SubjectViewSet,LessonViewSet,UserViewSet

router=routers.DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'standards', StandardViewSet, basename='standard')
router.register(r'subjects', SubjectViewSet,basename='subject')
router.register(r'lessons', LessonViewSet,basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
]