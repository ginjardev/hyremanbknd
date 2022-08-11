from dataclasses import fields
from unittest.mock import Base
from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate, get_user_model

 
class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        read_only_fields =  ('id', 'password',)

    def validate(self, data):
        """check email is not updated"""
        if self.instance:
            email = data.pop('email', None)
            if email and email != self.instance.email:
                raise serializers.ValidationError('Email can be set only once')
        return data

    def create(self, validated_data):
        """create and return a new user"""
        
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update user account"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """serializer for user authentication"""
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = False
    )

    def validate(self, attrs):
        """validate and authenticate users"""
        email = attrs.get('email')
        password = attrs.get('password')

        print(email, password)

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )
        print(user)
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Applicant
        fields = ('id', 'user', 'phone', 'date_of_birth', 'country', 'education', 'resume')
        read_only_fields = ('id', 'user',)

    def create(self, validated_data):
        """create profile"""
        user = self.context['request'].user
        if Applicant.objects.filter(id=user.id).exists():
            raise serializers.ValidationError('User has already been created')
        validated_data['user'] = user
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     """Update profile"""
    #     user = self.context['request'].user
    #     if user != instance.user:
    #         raise serializers.ValidationError('Might nor be your profile')
    #     return super().update(instance, validated_data)



class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Recruiter
        fields = ['id', 'user', 'phone', 'country', 'company']
        read_only_fields = ('id', 'user',)

    def create(self, validated_data):
        """create profile"""
        user = self.context['request'].user
        if Recruiter.objects.filter(id=user.id).exists():
            raise serializers.ValidationError('User has already been created')
        validated_data['user'] = user
        user.is_recuiter = True
        user.save()
        return super().create(validated_data)


class PasswordResetSerializer(serializers.ModelSerializer):
    """Serializer for Password reset"""
    user = serializers.PrimaryKeyRelatedField(
        queryset = get_user_model().objects.all()
    )

    class Meta:
        model = PasswordReset
        fields = (
            'reset_request',
            'validation_code',
            'verified_request',
            'reset_time',
            'user'
        )


class SelectedCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedCandidate
        fields = ['recruiter', 'applicant']