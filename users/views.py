from django.shortcuts import render
from rest_framework.response import Response
from users.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from users.serializers import ApplicantSerializer, RecruiterSerializer 

# Create your views here.


class ApplicantViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer 
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (applicant, created) = Applicant.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = ApplicantSerializer(applicant)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ApplicantSerializer(applicant, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    


    

class RecruiterViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (recruiter, created) = Recruiter.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = RecruiterSerializer(recruiter)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = RecruiterSerializer(recruiter, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# class ApplicantProfileUpdate():
