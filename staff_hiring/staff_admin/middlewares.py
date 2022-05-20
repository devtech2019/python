
from .models import *
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

User = get_user_model()

def login_middleware(get_response):   
    def my_middle(request):
        response = get_response(request)

        if request.user.is_authenticated:
            if "email" in request.session:
                u = User.objects.get(email=request.session['email'])
                if (u.soft_del_status==True) or (u.user_status==True):
                    auth.logout(request)
                    # del request.session['email']
                    return redirect('/login/')
               
                
        return response
    return my_middle






