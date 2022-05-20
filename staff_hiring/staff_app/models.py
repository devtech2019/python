from django.db import models
from staff_admin.models import User

# Create your models here.
class OTP(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    OTP=models.CharField(max_length=4)
    create_at=models.TimeField()
