from django.urls import path, include
from users.views import ApplicantViewSet, RecruiterViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('applicants', ApplicantViewSet)
router.register('recruiters', RecruiterViewSet)

urlpatterns = router.urls

