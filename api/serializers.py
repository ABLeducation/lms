from curriculum.models import Standard,Subject,Lesson
from rest_framework import serializers
from users.models import User

class standardserializer(serializers.HyperlinkedModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Standard
        fields="__all__"

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"

class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Lesson
        fields="__all__"

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields="__all__"