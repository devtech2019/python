from dataclasses import field
from django.db import models
from staff_admin.models import *

# Create your models here.
class Shift_Post(models.Model):

    serial_no = models.CharField(max_length=10)
    date=models.DateField(null=True)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField()
    position = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    text_field = models.TextField()
    break_time=models.TextField(null=True)
    wages = models.CharField(max_length=10, null=True)
    accepted = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobseeker')
    time_sheet=models.BooleanField(default=False)
    update_at=models.DateTimeField(auto_now_add=True)

class CompanyInfo(models.Model):
    PARTNERSHIP = (
        (1, 'Solo Proprietorship'),
        (2, 'Partnership'),
        (3, 'Corporation'),
        (4, 'Other'),
        
    )
    company_name=models.CharField(null=True,max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_slug = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    year_of_business = models.CharField(max_length=4)
    partnership  = models.CharField(choices=PARTNERSHIP,max_length=10,null=True)
    about_company = models.TextField(null=True)
    other = models.TextField()
    tax = models.CharField(max_length=250)


class Feedback(models.Model):
    RATING = (
        (1, 'Highly Dissatisfied'),
        (2, 'Dissatified'),
        (3, 'Nutral'),
        (4, 'Satisfied'),
        (5, 'Highly Satisfied'),
    )
    rating=models.CharField(max_length=10,choices=RATING)
    applicant=models.ForeignKey(User,on_delete=models.CASCADE,related_name='applicant')
    client=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='client')
    review=models.TextField()
    create_at=models.DateTimeField(auto_now_add=True)
    job_post=models.ForeignKey(Shift_Post,on_delete=models.SET_NULL,null=True)