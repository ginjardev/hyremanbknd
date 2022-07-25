from django.shortcuts import render
from users.models import *
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from users.serializers import ApplicantSerializer, RecruiterSerializer 

# Create your views here.


class ApplicantViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer 

class RecruiterViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
