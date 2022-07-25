from django.shortcuts import render
from rest_framework.response import Response
from users.models import *
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from users.serializers import ApplicantSerializer, RecruiterSerializer 

# Create your views here.


class ApplicantViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer 

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



    

class RecruiterViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        recruiter = Recruiter.objects.get(user_id=request.user.id)  
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)