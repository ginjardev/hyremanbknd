from unittest.mock import Base
from rest_framework import serializers
from .models import Applicant, Recruiter
from djoser.serializers import UserSerializer as BaseUserserializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','first_name', 'last_name', 'password', 'email']
 
class UserSerializer(BaseUserserializer):
    class Meta(BaseUserserializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ApplicantSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Applicant
        fields = ['id', 'user_id', 'phone', 'date_of_birth', 'country', 'education', 'resume']

class RecruiterSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Recruiter
        fields = ['id', 'user_id', 'phone', 'country', 'company']


