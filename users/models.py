from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_recruiter = models.BooleanField(default=False)
    


class Applicant(models.Model):
    HIGH_SCHOOL_CERTIFICATE = 'SSCE'
    DIPLOMA = 'Dip'
    BACHELOR_OF_SCIENCE = 'BSc'
    BACHELOR_OF_ARTS = 'BA'  
    BACHELOR_OF_ENGINEERING = 'BEng'  
    MASTER_OF_SCIENCE = 'MSc'  
    MASTER_OF_BUSINESS_ADMINISTRATION = 'MBA' 
    DOCTORAL_DEGREE = 'Dr'        
    EDUCATIONAL_LEVEL = [
        (HIGH_SCHOOL_CERTIFICATE, 'SSCE'),
        (DIPLOMA, 'Diploma'),
        (BACHELOR_OF_SCIENCE, 'Bachelor of Science'),
        (BACHELOR_OF_ARTS, 'Bachelor of Arts'),
        (BACHELOR_OF_ENGINEERING, 'Bachelor of Engineering'),
        (MASTER_OF_SCIENCE, 'Master of Science'),
        (MASTER_OF_BUSINESS_ADMINISTRATION, 'Master of Business Administration'),
        (DOCTORAL_DEGREE, 'Doctorate Degree'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_photo')
    phone = models.CharField(max_length= 13, blank=False, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=150, blank=False, null=False)
    education = models.CharField(max_length=33,choices=EDUCATIONAL_LEVEL, default=BACHELOR_OF_SCIENCE)
    resume = models.FileField(upload_to='resume_bank', blank=False, null = True)


    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length= 13, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=150, blank=False, null=False)
    company = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'



