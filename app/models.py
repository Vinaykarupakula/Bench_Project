from pyexpat import model
from statistics import mode
from django.db import models
import django
import datetime


# Create your models here.

class Employee(models.Model):
    
    id = models.AutoField(primary_key=True, null=False, default=0)
    # time_stamp = models.DateTimeField(auto_created=True, default=datetime.datetime.now(), null=True)
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length = 1000)
    emp_status = models.CharField(max_length=20)
    emp_type = models.CharField(max_length=100)
    skill_set = models.TextField()
    department = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(default=django.utils.timezone.now)
    project_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100,blank=True, null=True)
    previous_client = models.CharField(max_length=100)
    reason_for_offboard = models.TextField()
    email = models.EmailField()
    experience = models.CharField(max_length=100)
    comments = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.emp_name


