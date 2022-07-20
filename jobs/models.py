from django.db import models
from users.models import Recruiter

# Create your models here.
class Job(models.Model):
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    CONTRACT = 'CONT'
    INTERNSHIP = 'INT'
    JOB_TYPE = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (CONTRACT, 'Contract'),
        (INTERNSHIP, 'Internship'),
    ]
    title = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE, default=FULL_TIME)
    job_owner = models.ForeignKey(Recruiter, blank=False, null=False, on_delete=models.PROTECT)
    salary = models.IntegerField()
