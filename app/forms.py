from dataclasses import fields
from django import forms
from app.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["emp_name","emp_status","skill_set","end_date","experience","project_name","client_name"]

        
