from safedelete.models import SafeDeleteModel

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db.models import Q
from django.db.models.base import Model
from .manager import CustomUserManager
from django.contrib.auth.models import User
from .manager import CustomUserManager

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse
import datetime
from datetime import datetime
import uuid
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
import random
from django.core.files import File
from safedelete.models import SOFT_DELETE_CASCADE

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Cities(models.Model):
    name = models.CharField(max_length=200)
    state_id = models.CharField(max_length=30)
    state_code = models.CharField(max_length=30)
    country_id = models.CharField(max_length=20)
    country_code = models.CharField(max_length=20)

    latitude = models.FloatField()
    longitude = models.FloatField()


class States(models.Model):
    name = models.CharField(max_length=200)
    country_id = models.CharField(max_length=20)
    country_code = models.CharField(max_length=20)
    fips_code = models.CharField(max_length=10)
    iso2 = models.CharField(max_length=10)
    state_code = models.CharField(max_length=20)


class Country(models.Model):
    name = models.CharField(max_length=200)
    ios3 = models.CharField(max_length=20)
    iso2 = models.CharField(max_length=20)
    phonecode = models.CharField(max_length=20)
    capital = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    native = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100)
    timezones = models.CharField(max_length=100)
    tld = models.CharField(max_length=100)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    emoji = models.CharField(max_length=100)
    emojiU = models.CharField(max_length=100)


class Category(models.Model):
    DAY_CHOISE = (
        ("sun", "Sunday"),
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
    )

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    week_hour = models.CharField(max_length=4)
    leave_day = models.CharField(choices=DAY_CHOISE, max_length=200)
    shift_diffrence = models.CharField(max_length=3)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    soft_del_status = models.BooleanField(default=False)

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


class User(AbstractUser):
    # _safedelete_policy = SOFT_DELETE_CASCADE

    USER_TYPE = (
        ("subadmin", "Subadmin"),
        ("admin", "Admin"),
        ("employer", "employer"),
        ("applicant", "applicant"),
    )
    roll = models.CharField(
        max_length=10,
        choices=USER_TYPE,
    )
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    company = models.CharField(max_length=100, null=True, blank=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    price = models.CharField(max_length=10, default=None, null=True, blank=True)

    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    image = models.ImageField(
        null=True, blank=True, upload_to="media", default="face1.jpg"
    )
    mobile_number = models.CharField(
        max_length=50,
    )
    landline = models.CharField(max_length=20, null=True)
    country_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    experience = models.CharField(max_length=20, null=True)
    address = models.CharField(null=True, max_length=300)
    address2 = models.CharField(null=True, max_length=300)

    user_status = models.BooleanField(null=True, default=False)
    company_profile_status = models.BooleanField(null=True, default=False)

    soft_del_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    OTP_string = models.CharField(max_length=10, null=True)
    reset_time_link = models.DateTimeField(auto_now_add=True)
    OTP = models.CharField(max_length=10)
    OTP_create_at = models.DateTimeField(auto_now_add=True)
    exp_year = models.CharField(max_length=5, null=True)
    exp_month = models.CharField(max_length=5, null=True)
    mob_no_verified = models.BooleanField(default=False)
    position = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    email_verified = models.BooleanField(default=False)
    mail_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)
    # is_applicant = models.BooleanField()
    # USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def soft_delete(self):
        self.soft_del_status = True
        self.save()

    def __str__(self):
        return self.email


class email_templates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    sub = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default=uuid.uuid4, unique=True)
    content = models.TextField()
    soft_del_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


class AppWebIntro(models.Model):
    title = models.TextField()
    textarea = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="intro/")
    slug = models.SlugField(max_length=50, default=uuid.uuid4, unique=True)


class pages(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default=uuid.uuid4, unique=True)
    text = models.TextField()
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="pages/")
    soft_del_status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(null=True)

    def __str__(self):
        return self.title

    # Update Slug with timestamp in hash
    def save(
        self,
        *args,
        **kwargs,
    ):
        qs_exists = pages.objects.filter(slug=self.slug).exists()
        if qs_exists:
            now = datetime.now()
            current_time = now.timestamp()
            current_time_hash = hash(current_time)
            u = pages.objects.filter(slug=self.slug).update(
                slug=self.slug + str(current_time_hash)
            )
        self.slug = slugify(self.title)
        super(pages, self).save(*args, **kwargs)

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


class AboutUs(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="aboutus/")
    slug = models.SlugField(max_length=50, unique=True, default=uuid.uuid4)
    discripion = models.TextField()

    soft_del_status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(null=True)

    def __str__(self):
        return self.title


class meet_our_team(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="aboutus/")
    slug = models.CharField(max_length=50, default=uuid.uuid4, unique=True)
    discripion = models.TextField()

    soft_del_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Global_setting(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)

    email = models.EmailField(unique=True)
    img = models.ImageField(null=True, blank=True, upload_to="global/")
    facebook_link = models.CharField(max_length=50)
    instagram_link = models.CharField(max_length=50)
    pintrest_link = models.CharField(max_length=50)
    twitter_link = models.CharField(max_length=50)
    linkdin_link = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default=uuid.uuid4, unique=True)
    discripion = models.TextField()
    soft_del_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


@receiver(pre_delete, sender=Global_setting)
def delete_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.img:
        instance.img.delete(False)


class Qr_Code(models.Model):
    Qr_url = models.URLField()
    Qr_image = models.ImageField(null=True, blank=True, upload_to="Qr_image")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.Qr_url)
        canvas = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.Qr_image.save(f"image{random.randint(0, 9999)}", File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Training(models.Model):
    training_name = models.CharField(max_length=255)
    Status = models.BooleanField(default=False)
    user = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)

    soft_del_status = models.BooleanField(default=False)

    def __str__(self):
        return self.training_name

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


class ContactUs(models.Model):
    First_name = models.CharField(max_length=255, null=True)
    Last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, default=uuid.uuid4, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    sub = models.CharField(max_length=100, null=True)
    soft_del_status = models.BooleanField(default=False)

    def __str__(self):
        return self.First_name

    def soft_delete(self):
        self.soft_del_status = True
        self.save()


class ContentManagement(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    slug = models.CharField(max_length=100)



class RoomCreate(models.Model):
  room_name=models.CharField(max_length=10)
  f_person = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='first_person')
  s_person = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name='second_person')
  create_at=models.DateTimeField(auto_now_add=True)


class Message(models.Model):
  username = models.CharField(max_length=255)
  room = models.ForeignKey(RoomCreate,on_delete=models.CASCADE)
  content = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)
  send_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
  reciever_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_query_name='reciever')

  class Meta:
    ordering = ('date_added',)