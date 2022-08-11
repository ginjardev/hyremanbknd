from venv import create
from django import views
from django.urls import path, include
from users.views import ApplicantViewSet, RecruiterViewSet, CreateUserView, CreateTokenView, SelectedApplicantViewSet
from .forms import ApplicantForm

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'applicants', ApplicantViewSet)
router.register(r'recruiters', RecruiterViewSet)
router.register(r'selectedapplicants', SelectedApplicantViewSet)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('', include(router.urls))
]

