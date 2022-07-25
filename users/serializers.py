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
    class Meta:
        model = Applicant
        fields = ['id', 'phone', 'country', 'education', 'resume']

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'phone', 'country', 'company']


