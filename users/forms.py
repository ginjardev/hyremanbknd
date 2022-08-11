from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import *


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['user', 'phone', 'country', 'region', 'education', 'resume']
    