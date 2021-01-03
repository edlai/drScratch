from rest_framework.serializers import Serializer, FileField
from django.contrib.auth.models import User
from rest_framework import serializers
from models import Mastery


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class MasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mastery

class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']