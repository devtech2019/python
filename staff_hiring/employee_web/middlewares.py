
from .models import *
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect

User = get_user_model()

EXEMPT_PATH = ['/']

class social_middleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
           
    
            us = SocialAccount.objects.get(user_id=request.user.id)
            u = User.objects.get(id=us.user_id)
            u.roll='employer'
            u.fname = u.first_name
            u.lname = u.last_name  
            u.save()
            print(u.company_profile_status,"fffffffffffffffffffffffffffffffffffff")
            if u.company_profile_status==False:
              if not request.path == reverse('/'):
                return redirect(reverse('/profile/company-profile/' + u.slug))

            else:
                pass
            return response
        except:
            return response

  



        


# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         response = self.get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response
