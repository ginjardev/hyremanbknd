# Generated by Django 4.0.6 on 2022-07-27 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_recruiter_applicant'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_recruiter',
            field=models.BooleanField(default=False),
        ),
    ]
