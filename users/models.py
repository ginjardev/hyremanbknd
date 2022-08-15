from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name,is_recruiter, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Password is required")
        if not first_name and last_name:
            raise ValueError("First and last name is required")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, is_recruiter=is_recruiter,)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # def create_recruiter(self, email, first_name, last_name, password=None, **extra_fields):
    #     """Create Recruiter profile"""
    #     user = self.create_user(email, first_name, last_name, password=password)
    #     user.is_recruiter = True
    #     user.save(using=self._db)

    #     return user


    def create_superuser(self, email, password, first_name='hyreman', last_name='admin', is_recruiter=True):
        """Create superuser profile"""
        user = self.create_user(email, first_name, last_name, is_recruiter, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_recruiter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    objects = UserManager()
    USERNAME_FIELD = 'email'

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Tool(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Applicant(models.Model):
    HIGH_SCHOOL_CERTIFICATE = 'SSCE'
    DIPLOMA = 'Diploma'
    BACHELOR_OF_SCIENCE = 'Bachelor of Science'
    BACHELOR_OF_ARTS = 'Bachelor of Arts'  
    BACHELOR_OF_ENGINEERING = 'Bachelor of Engineering'  
    MASTER_OF_SCIENCE = 'Master of Science'  
    MASTER_OF_BUSINESS_ADMINISTRATION = 'Master of Business Administration' 
    DOCTORAL_DEGREE = 'Doctorate Degree'        
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

    EXPERIENCE_LEVEL = [
        ('Entry Level', 'Entry Level'),
        ('Mid Level', 'Mid Level'),
        ('Senior Level', 'Senior Level'),
    ]

    MALE = 'M'
    FEMALE = 'F'

    GENDER_OPTION = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION, default=MALE)
    image = models.ImageField(upload_to='profile_photo', blank=True)
    phone = models.CharField(max_length= 13, blank=False, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=150, blank=False, null=False)
    education = models.CharField(max_length=255,choices=EDUCATIONAL_LEVEL, default=BACHELOR_OF_SCIENCE)
    resume = models.FileField(upload_to='resume_bank', blank=False, null = True,)
    skills = models.ManyToManyField(Skill, blank=True, related_name='applicants')
    experience_level = models.CharField(max_length=100, choices=EXPERIENCE_LEVEL, default='Entry Level', verbose_name='Experience Level')
    tools = models.ManyToManyField(Tool, blank=True, default='Google Workspace')
   


    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'



class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length= 13, blank=False, null=False)
    company_size = models.IntegerField(blank=False, null=False, default=1)
    country = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=150, blank=False, null=False)
    company = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

class PasswordReset(models.Model):

    reset_request = models.BooleanField(default=False)
    verified_request = models.BooleanField(default=False)
    validation_code = models.CharField(max_length=255, blank=True)
    reset_time = models.DateTimeField(auto_now=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset',
        default=None
    )

    def __str__(self):
        return self.user.name





class SelectedCandidate(models.Model):
    class Meta:
        unique_together = (('recruiter', 'applicant'))
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='SelectedCandidate_recruiter')
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='SelectedCandidate_applicant')