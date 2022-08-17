from json import tool
from rest_framework.response import Response
from users.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from users.serializers import ApplicantSerializer, AuthTokenSerializer, RecruiterSerializer, SelectedCandidateSerializer, UserSerializer, PasswordResetSerializer , SkillSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import random
from datetime import *



class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def raise_error(self,msg):
        msg = [msg]
        error_data = {'errors': msg}
        raise serializers.ValidationError(error_data, code='registration')


    def perform_create(self, serializer):
        """creating a new user"""

        validated_data = self.request.data

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        is_recruiter = validated_data.get('is_recruiter', False)

        if password != confirm_password:
            self.raise_error('Passwords does not match')
        if len(password) < 6:
            self.raise_error('Password should be 6 or more characters')

        user = serializer.save(first_name=first_name, last_name=last_name, email = email, password = password, is_recruiter=is_recruiter)
        
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  
        headers = self.get_success_headers(serializer.data) 

        response = serializer.data
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class CreateTokenView(ObtainAuthToken):
    """creating a token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        validated_data = self.request.data

        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        user_data = UserSerializer(user)

        response = {
            'token': token.key,
            'user': user_data.data,
        }

        return Response(response)




class ApplicantViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet, ListModelMixin):
    serializer_class = ApplicantSerializer 
    queryset = Applicant.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
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
        print(serializer.data[0]['skills'])
        return Response(serializer.data)    


    def get_queryset(self):
        """Return objects for the current authenticated user"""
        queryset = self.queryset

        education = self.request.query_params.get('education') or ""
        country = self.request.query_params.get('country') or ""
        region = self.request.query_params.get('region') or ""
        gender = self.request.query_params.get('gender') or ""
        skills = self.request.query_params.get('skills_name') or ""
        experience_level = self.request.query_params.get('experience_level') or ""
        tools = self.request.query_params.get('tools') or ""

        if education:
            queryset = queryset.filter(education=education)
        if country:
            queryset = queryset.filter(country=country)
        if region:
            queryset = queryset.filter(region=region)
        if gender:
            queryset = queryset.filter(gender=gender)
        if skills:
            queryset = queryset.filter(skills=skills)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        if tools:
            queryset = queryset.filter(tools=tools)

        return queryset.distinct()


    

class RecruiterViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
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

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SelectedApplicantViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SelectedCandidate.objects.all()
    serializer_class = SelectedCandidateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class SkillList(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)



# @api_view(['POST'])
# def password_reset(request):
#     """send email to user"""
#     response_format = {}
#     data = request.data
    
#     try:
#         snippet = get_user_model().objects.get(email=data['email'])
#     except get_user_model().DoesNotExist:
#         errors = 'User with email does not exist'
#         return Response(data=errors, status = status.HTTP_404_NOT_FOUND)


#     userData = snippet 
#     random_number = random.randint(100000, 999999)
#     userData.code = random_number
#     password_reset_data = {
#         'reset_request': True,
#         'validation_code': random_number,
#         'reset_time': timezone.now(),
#         'user': userData.id,
#     }

#     try:
#         user_password_reset = PasswordReset.objects.get(user=userData.id)
#         if user_password_reset:
#             serializer = PasswordResetSerializer(
#                 user_password_reset, data=password_reset_data
#             )
#     except PasswordReset.DoesNotExist:
#         serializer = PasswordResetSerializer(data=password_reset_data)

#     if serializer.is_valid():
#         serializer.save()
#         mock = mock_if_true()

#         if not mock:
#             mail = email_compose(type="reset-password", data=userData)
#             send_mail_sendgrid(email=data['email'], subject=mail['subject'], name=userData.name,
#             code=random_number)
#             message = 'Reset code sent successfully to email provided'
#             return Response(data=message, status=status.HTTP_200_OK)
#         else: 
#             message = f'Reset code sent successfully to email provided (mock) {random_number}'
#             return Response(data=message, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
