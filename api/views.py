from rest_framework import viewsets
from .serializers import standardserializer,SubjectSerializer,LessonSerializer,UserSerializer
from curriculum.models import Standard,Subject,Lesson
from users.models import User

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class StandardViewSet(viewsets.ModelViewSet):
    queryset=Standard.objects.all()
    serializer_class=standardserializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset=Lesson.objects.all()
    serializer_class=LessonSerializer
    