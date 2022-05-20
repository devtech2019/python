from distutils.command.upload import upload
from operator import mod
from typing import Tuple
from venv import create
from django.db import models
from employee_web.models import *

# Create your models here.
from django.db import models
from staff_admin.models import *

# Create your models here.


class ApplicantDeatails(models.Model):
    STATUS = (
        (1, "APPORVE"),
        (2, "QUERY"),
        (3, "PENDING"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    vaccinated = models.CharField(max_length=100)

    first_dose = models.DateField(default="2022-03-01")
    second_dose = models.DateField(default="2022-03-01")
    image = models.ImageField(
        null=True, blank=True, upload_to="vaccination")
    booster_dose = models.CharField(max_length=100)
    address = models.CharField(max_length=250, null=True)
    position = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="applicant_info_position",
    )
    Mnc_pin = models.CharField(max_length=100, verbose_name="Mnc pin")

    dob = models.DateField()
    recitation = models.BooleanField()
    recitation_desc = models.TextField(null=True)
    enhance_dbc = models.CharField(max_length=150, null=True)
    enhance_dbc_issue = models.DateField(null=True)
    dbc_status = models.CharField(max_length=150, null=True)
    work_checkes = models.TextField(null=True)
    work_preference = models.TextField(null=True)
    emergency_no = models.CharField(max_length=20, null=True)
    training = models.ForeignKey(Training, null=True, on_delete=models.SET_NULL)
    training_start_date = models.DateField(null=True)
    training_end_date = models.DateField(null=True)
    vaccination_status = models.BooleanField(null=True, default=False)

    status = models.CharField(choices=STATUS, max_length=10, default=3)


class TimeSheet(models.Model):
    STATUS = (
        (1, "APPORVE"),
        (2, "REJECT"),
        (3, "PENDING"),
    )
    RATING = (
        (1, "SO-WOREST"),
        (2, "WOREST"),
        (3, "GOOD"),
        (4, "VERY GOOD"),
        (5, "EXCELLENT"),
    )

    applicant = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="time_sheet_applicant"
    )
    shift = models.ForeignKey(Shift_Post, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)
    time_in = models.TimeField(null=True)
    time_out = models.TimeField(null=True)
    break_time = models.CharField(null=True, max_length=6)
    authorized_by = models.CharField(max_length=100, null=True)
    app_position = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="app_position"
    )
    emp_position = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="emp_position"
    )

    approve_date = models.DateField(null=True)
    approved_by = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS, max_length=10, default=3)
    applicant_review = models.TextField(null=True)
    sign_img = models.ImageField(upload_to="signature", default="face1.jpg")
    submit_status = models.BooleanField(default=False)
    employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="time_sheet_employee"
    )
    employee_review = models.TextField(null=True)
    rating = models.CharField(choices=RATING, max_length=10, default=3, null=True)
    resolve_status = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)


class ShiftLike(models.Model):
    shift = models.ForeignKey(
        Shift_Post, on_delete=models.CASCADE, related_name="shift_like"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    like = models.BooleanField(default=False)


class Query(models.Model):
    timesheet = models.ForeignKey(TimeSheet, on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="query_admin", null=True
    )
    employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="query_employee", null=True
    )
    date = models.DateField()
    name = models.CharField(max_length=250, null=True)
    postion = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="query_position", null=True
    )
    create_at = models.DateTimeField(auto_now_add=True)


class QueryMessage(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="qurery_message_sender"
    )
    reciver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="qurery_message_reciever",
    )
    create_at = models.DateTimeField(auto_now_add=True)
    # name=models.CharField(max_length=250,null=True)
