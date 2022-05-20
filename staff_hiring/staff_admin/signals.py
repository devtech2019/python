# from django.db.models import Q
# from django.db.models.signals import pre_save, post_save
# from .models import User, Thread
# from django.dispatch import receiver
# from django.utils import timezone


# @receiver(post_save, sender=User)
# def user_pre_save(sender,created, instance, *args, **kwargs):
#     if instance.roll == "applicant":
#         users = User.objects.filter(roll="admin")
#         if users.exists():
#             for user in users:
#                 Thread.objects.get_or_create(first_person=instance, second_person=user)
#     if instance.roll == "employer":
#         users = User.objects.filter(roll="admin")
#         if users.exists():
#             for user in users:
#                 Thread.objects.get_or_create(first_person=instance, second_person=user)
#     if instance.roll == "admin":
#         users = User.objects.filter(Q(roll="applicant") | Q(roll="employer"))
#         if users.exists():
#             for user in users:
#                 Thread.objects.get_or_create(first_person=instance, second_person=user)
