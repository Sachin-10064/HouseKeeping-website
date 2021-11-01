from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_Admin = models.BooleanField(default=False)

class ContactUs(models.Model):
    name = models.CharField(max_length=45,null=False)
    email = models.CharField(max_length=45, null=False)
    query = models.TextField(null=False)
    answer =models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now, editable=False, )

class Feedback(models.Model):
    username = models.CharField(max_length=20, null=False)
    feedback_text = models.TextField(null=False)
    rating = models.IntegerField(null=False)
    date = models.DateTimeField(default=timezone.now, editable=False, )

class Complaint(models.Model):
    username = models.CharField(max_length=20, null=False)
    subject = models.CharField(max_length=20, null=False)
    complaint_text = models.TextField(null=False)
    status = models.CharField(max_length=10, null=False, default="")
    date = models.DateTimeField(default=timezone.now, editable=False, )

class Job(models.Model):
    jobid = models.CharField(max_length=100, null=False, primary_key=True)
    postname = models.CharField(max_length=100, null=False)
    eligibility = models.CharField(max_length=45)
    no_of_post = models.IntegerField(null=False)
    age_limit = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=45, null=False)
    date = models.DateTimeField(default=timezone.now, editable=False, )
    phone = models.IntegerField(null=True)

class UserProfile(models.Model):
    username = models.CharField(max_length=45, null=False, primary_key=True)
    city = models.CharField(max_length=45, null=False)
    address = models.TextField(null=False)
    phone = models.IntegerField(null=False)
    gender = models.CharField(max_length=6, null=False)
    date = models.DateTimeField(default=timezone.now, editable=False, )

class EmployeeType(models.Model):
    employee_type = models.CharField(max_length=45, null=False)
    description = models.TextField(null=False)

class CompanyAdmin(models.Model):
    customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=45, null=False)
    address = models.TextField(null=False)
    phone = models.IntegerField(null=False)
    gender = models.CharField(max_length=6, null=False)
    experience = models.CharField(max_length=20, null=False)
    admin_pic = models.ImageField(max_length=100, upload_to="housekeeping/admin", default="")

class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=100, null=False, primary_key=True)
    owner_name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=45, null=False)
    address = models.TextField(null=False)
    phone = models.IntegerField(null=False)
    email = models.CharField(max_length=100, null=False,)
    about = models.TextField(null=False)
    visting_hours = models.CharField(max_length=20, null=False)
    working_hours = models.CharField(max_length=20, null=False)

class Employee(models.Model):
    employee_id = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=45, null=False)
    address = models.TextField(null=False)
    phone = models.IntegerField(null=False)
    gender = models.CharField(max_length=6, null=False)
    date_of_join = models.DateTimeField(default=timezone.now, editable=False, )
    experience = models.CharField(max_length=20, null=False)
    employee_type = models.CharField(max_length=40, null=True)
    admin_pic = models.ImageField(max_length=100, upload_to="housekeeping/employee", default="")
    status = models.CharField(max_length=10, null=False, default="Free")
    request_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

class EmployeeRequest(models.Model):
    employee_type = models.CharField(max_length=45, null=False)
    username = models.CharField(max_length=100, null=False)
    noOfEmployee = models.IntegerField(null=False)
    date_of_request = models.DateTimeField(default=timezone.now, editable=False, )
    request_text = models.TextField(null=False)
    date_of_answer = models.DateTimeField(null=True, blank=True)
    answer = models.TextField(null=True)

class EmployeeAssignment(models.Model):
    assign_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(EmployeeRequest, on_delete=models.CASCADE, default=0)
    # employee_id = models.CharField(max_length=45, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    date = models.DateField(default=timezone.now, editable=False, )