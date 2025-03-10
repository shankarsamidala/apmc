from django.contrib.auth.models import AbstractUser
from django.db import models

class Faculty(AbstractUser):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    ]
    
    emp_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class StudentCall(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="calls")
    student_name = models.CharField(max_length=255)
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True, blank=True)

    INTER_GROUP_CHOICES = [
        ('MPC', 'MPC'),
        ('BiPC', 'BiPC'),
        ('CEC', 'CEC'),
        ('MEC', 'MEC'),
        ('HEC', 'HEC'),
        ('Other', 'Other'),
    ]
    inter_group = models.CharField(max_length=50, choices=INTER_GROUP_CHOICES, null=True, blank=True)
    inter_marks = models.IntegerField(null=True, blank=True)
    exam_rank = models.CharField(max_length=50, null=True, blank=True)
    
    rmarks = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    college = models.CharField(max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=255, null=True, blank=True)

    CALL_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Answered'),
        ('NA', 'Not Answered'),
        ('WN', 'Wrong Number'),
 
    ]
    call_1_status = models.CharField(max_length=2, choices=CALL_STATUS_CHOICES, default='P')
    
    STUDENT_STATUS_CHOICES = [
        ('NI', 'Not Interested'),
        ('WD', 'Willing to Degree'),
        ('WE', 'Willing to Engineering'),
        ('ND', 'Not Decided'),
        ('J', 'Joined'),
    ]
    status = models.CharField(max_length=2, choices=STUDENT_STATUS_CHOICES, default='ND')

    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.student_name} - {self.faculty.full_name}"