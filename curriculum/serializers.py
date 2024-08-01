from curriculum.models import *
from rest_framework import serializers

class LectureRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureRating
        fields = ('lecture', 'user', 'rating', 'date_rated')