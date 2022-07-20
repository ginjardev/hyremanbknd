# Generated by Django 4.0.6 on 2022-07-20 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_recruiter_applicant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('job_type', models.CharField(choices=[('FT', 'Full Time'), ('PT', 'Part Time'), ('CONT', 'Contract'), ('INT', 'Internship')], default='FT', max_length=10)),
                ('salary', models.IntegerField()),
                ('job_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.recruiter')),
            ],
        ),
    ]