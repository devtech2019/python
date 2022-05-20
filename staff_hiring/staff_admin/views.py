from ast import Pass
from http import cookies


import pgeocode
from os import PRIO_PGRP
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from atexit import register
from email import message
from operator import sub
from re import template
from django.shortcuts import render
from geopy.geocoders import Nominatim
import hashlib
from rest_framework.response import Response

import geopandas

from datetime import timedelta
from django.core.signing import TimestampSigner
from time import gmtime, strftime

# Create your views here.
from django import http
from django.contrib.auth import hashers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.defaultfilters import add

from applicant_web.models import *
from .models import *

# from staff_admin.models import training_user
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
import math
import random
from .helpers import *
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.db.models import Q

# from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as login_check
from django.conf import settings
import json
from django.db.models import Count
import calendar
from django.utils import timezone
import qrcode
import qrcode.image.svg
from django.views.decorators.cache import never_cache
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
from django.utils.timezone import utc
from django import template
from django.contrib.auth.models import Group, Permission
from django import template
from encrypted_id import ekey
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from employee_web.models import *

# Count Employer and Applicant and Jobs
# register = template.Library()


# @register.filterFajax
# def to_char(value):
#     return chr(98-value)


@login_required(login_url="/admin/")
def dashboard(request):

    userdata = User.objects.all()
    count_emp = User.objects.filter(soft_del_status=0, roll="employer").count()
    count_sub = User.objects.filter(soft_del_status=0, roll="Subadmin").count()
    count_app = User.objects.filter(soft_del_status=0, roll="applicant").count()
    count_user = count_app + count_emp
    employer_query = f"""
        select id, count(*) as total,strftime("%%m",created_at) as month 
        from staff_admin_user where roll="employer" and soft_del_status=0 group by strftime("%%m",created_at);

    """
    employer_user_count = User.objects.raw(employer_query)
    print(employer_user_count, "dddddddddddddddddddddddddd")

    applicant_query = f"""
                select id, count(*) as total,strftime("%%m",created_at) as month 
                from staff_admin_user where roll="applicant" and soft_del_status=0 group by strftime("%%m",created_at);
            """
    applicant_user_count = User.objects.raw(applicant_query)

    i = 0
    append_in_month_name = []
    employer_data = []
    while i <= 11:
        i += 1

        obj = dict()
        obj.update(
            {"employer_total": 0, "month": calendar.month_name[i], "applicant_total": 0}
        )
        convert_in_month_name = calendar.month_name[i]
        employer_data.append(obj)
    for user in employer_user_count:
        employer_data[int(user.month) - 1]["employer_total"] = user.total

    for user in applicant_user_count:
        employer_data[int(user.month) - 1]["applicant_total"] = user.total
    context = {
        "userdata": userdata,
        "count_user": count_user,
        "count_emp": count_emp,
        "count_app": count_app,
        "employer_data": employer_data,
        "employer_user_count": employer_user_count,
        "count_sub": count_sub,
    }
    return render(request, "base/dashboard.html", context)


# Admin Login Function with SuperUser
@never_cache
def login(request):
    try:
        if request.method == "POST":
            email = request.POST.get("Email")
            password = request.POST.get("password")
            v = User.objects.get(email=email)
            request.session["email"] = email
            user = auth.authenticate(email=email, password=password)

            if user.roll == "Subadmin" or user.is_superuser:
                if user is None:
                    messages.error(request, "Invalid username or password ")
                    return redirect("/admin/")

                if user.is_superuser == True:
                    auth.login(request, user)
                    return redirect("/admin/dashboard/")

                if user.email:

                    if v.user_status == False:
                        # request.session['subadmin'] = v.soft_del_status
                        # print(request.session['subadmin'], "session subadminnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")

                        auth.login(request, user)

                        return redirect("/admin/dashboard/")

                    elif user.email:
                        auth.logout(request)
                        messages.error(request, "Permission denied")

                        return redirect("/admin/")
                    else:

                        auth.logout(request)
                        messages.error(request, "Permission denied")

                        return redirect("/admin/dashboard/")

                elif user.roll == "Subadmin " is None:
                    messages.error(request, "Invalid Username or Password ")
                    return redirect("/admin/")

            else:
                messages.error(request, "Invalid Username or Password ")
                return redirect("/admin/")

        else:
            if request.user.is_active == True:
                return redirect("/admin/dashboard/")
            else:
                return render(request, "auth/login.html")
    except:
        messages.error(
            request,
            "Invalid Username or Password ",
        )

        return render(request, "auth/login.html")


# Admin Logout function
@login_required(login_url="/admin/")
def logout(request):
    auth.logout(request)
    return redirect("/admin/")


# Display Employer data
@permission_required("staff_admin.view_user", raise_exception=True)
@login_required(login_url="/admin/")
def employer_user_data(request):

    try:
        emp_user = User.objects.filter(roll="employer", soft_del_status=0).order_by(
            "-created_at"
        )
        userdata = User.objects.all()
        page = request.GET.get("page", 1)
        paginator = Paginator(emp_user, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(
            request,
            "user/employer/employer.html",
            {"emp_user": emp_user, "users": users, "userdata": userdata},
        )
    except:
        messages.error(request, "Something Went Wronge")
        return render(
            request,
            "user/employer/employer.html",
        )


def employer_view_data(request, slug):
    emp_user = User.objects.get(slug=slug, roll="employer")
    userdata = User.objects.all()
    return render(
        request, "user/employer/view.html", {"emp_user": emp_user, "userdata": userdata}
    )


# Employer Status Via Ajax
@login_required(login_url="/admin/")
def employer_user_ajax(request, id):
    status = request.POST.get("select")
    if status:

        ob = User.objects.filter(id=id).update(user_status=status)
        x = User.objects.get(id=id)
        email = x.email
        e = email_templates.objects.get(id=2)
        content = e.content
        # html_page = urllib2.urlopen(url)

        if status == "0":
            send_to = [email]

            subject = e.sub
            content = e.content
            name = x.first_name + " " + x.last_name

            user_status = "Accepted"
            t = strip_tags(content)
            c = t.replace("{name}", name)
            msg = c.replace("{LINK}", user_status)
            sendMail(subject, msg, send_to)
            return JsonResponse(
                {"status": "success", "message": "Status changed successfully !!!!"},
                status=200,
            )

        else:
            send_to = [email]
            subject = e.sub
            content = e.content
            name = x.first_name + " " + x.last_name

            user_status = "Rejected"

            t = strip_tags(content)

            c = t.replace("{name}", name)

            msg = c.replace("{LINK}", user_status)

            sendMail(subject, msg, send_to)
            return JsonResponse(
                {"status": "success", "message": "Status changed successfully !!!!"},
                status=200,
            )

    else:
        return JsonResponse(
            {"status": "error", "message": "Status changed successfully !!!!"},
            status=200,
        )


# Applicant Status Via Ajax
@login_required(login_url="/admin/")
def applicant_user_ajax(request, id):
    status = request.POST.get("select")
    ob = User.objects.filter(id=id).update(user_status=status)

    x = User.objects.get(id=id)
    email = x.email
    e = email_templates.objects.get(id=2)
    if status == "0":
        send_to = [email]

        subject = e.sub
        content = e.content + "     " + "Accepted"
        sendMail(subject, content, send_to)
        return JsonResponse(
            {"status": "success", "message": "Status changed successfully !!!!"},
            status=200,
        )
    else:
        send_to = [email]

        subject = e.sub
        content = e.content + "     " + "Rejected"
        sendMail(subject, content, send_to)
        return JsonResponse(
            {"status": "error", "message": " Status changed successfully !!!!"},
            status=200,
        )


# get company data  Via Ajax
def employer_data_pdf(request, slug):
    if request.method == "POST":
        cname = request.POST.get("cname")
        print(cname, "companyyyyyyyyyyyyyyyyyyyyyy")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        Fax = request.POST.get("Fax")
        caddress = request.POST.get("caddress")
        year_of_business = request.POST.get("year_of_business")
        sole_proprietorship = request.POST.get("solo")
        print(sole_proprietorship, "sssssssssssssssssssssssssssss")
        partnership = request.POST.get("partnership")
        print(partnership, "sssssssssssssssssssssssssssss")
        corporation = request.POST.get("corporation")
        print(corporation, "sssssssssssssssssssssssssssss")

        redio = request.POST.get("propertytype")
        print(redio, "sssssssssssssssssssssssssssss")

        other = request.POST.get("other")
        tax = request.POST.get("tax")
        if CompanyInfo.objects.filter(phone_number=phone):
            return JsonResponse(
                {"status": "error", "message": " Mobile Number Allready Exits    !!!!"},
                status=404,
            )
        elif CompanyInfo.objects.filter(email=email):
            return JsonResponse(
                {"status": "error", "message": " Email Allready exits  !!!!"},
                status=404,
            )

        obj = User.objects.get(slug=slug)

        user = obj.id
        try:
            print("aaaaaaaaaaaaaaa")
            if redio == "1":
                print("dddddddddddddd")

                com = CompanyInfo.objects.create(
                    user_id=user,
                    name=cname,
                    phone_number=phone,
                    fax=Fax,
                    email=email,
                    address=caddress,
                    year_of_business=year_of_business,
                    about_company=sole_proprietorship,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                obj.company_profile_status = True
                obj.save()
                # com.save()
                return JsonResponse(
                    {"status": "Success", "message": " Details  Saved  !!!!"},
                    status=200,
                )

            elif redio == "2":
                com = CompanyInfo.objects.create(
                    user_id=user,
                    name=cname,
                    phone_number=phone,
                    fax=Fax,
                    email=email,
                    address=caddress,
                    year_of_business=year_of_business,
                    about_company=partnership,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                obj.company_profile_status = 1
                obj.save()
                com.save()
                return JsonResponse(
                    {"status": "Success", "message": " Details  Saved  !!!!"},
                    status=200,
                )

            elif redio == "3":
                com = CompanyInfo.objects.create(
                    user_id=user,
                    name=cname,
                    phone_number=phone,
                    fax=Fax,
                    email=email,
                    address=caddress,
                    year_of_business=year_of_business,
                    # about_company=partnership,
                    about_company=corporation,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                obj.company_profile_status = 1
                obj.save()
                com.save()
                return JsonResponse(
                    {"status": "Success", "message": " Details  Saved  !!!!"},
                    status=200,
                )

        except:
            messages.error(request, "Something Went Wrong")
            return redirect("/admin/employer_detail_list/" + slug)

        # print(cname, phone, Fax, caddress, year_of_business,solo,partnership,corporation,other,tax,"ddddddddddddddddddddddddddddd")

        messages.success(request, "Company details are saved succesfully !!!! ")
        return JsonResponse(
            {"status": "Success", "message": " Details  Saved  !!!!"}, status=200
        )

    return JsonResponse({"status": "error", "message": "  NO changed !!!!"})


#   try:

#                 users = CompanyInfo.objects.create(
#                     user_id=user.id,
#                     name=name,
#                     phone_number=phone_number,
#                     fax=fax,
#                     email=email,
#                     address=address,
#                     year_of_business=year_in_bussiness,
#                     about_company=sole_proprietorship,
#                     Partnership=redio,
#                     other=other,
#                     tax=tax,
#                 )
#                 users.save()

#                 user.company_profile_status = True
#                 user.save()
#                 messages.success(request, "Company details saved succssfully !!!! ")
#                 return redirect("/login/")
#             elif redio == "2":
#                 users = CompanyInfo.objects.create(
#                     user_id=user.id,
#                     name=name,
#                     phone_number=phone_number,
#                     fax=fax,
#                     email=email,
#                     address=address,
#                     year_of_business=year_in_bussiness,
#                     about_company=partnership,
#                     # about_company=corporation,
#                     Partnership=redio,
#                     other=other,
#                     tax=tax,
#                 )
#                 users.save()

#                 user.company_profile_status = True
#                 user.save()
#                 messages.success(request, "Company details saved succssfully !!!! ")
#                 return redirect("/login/")
#             elif redio == "3":

#                 users = CompanyInfo.objects.create(
#                     user_id=user.id,
#                     name=name,
#                     phone_number=phone_number,
#                     fax=fax,
#                     email=email,
#                     address=address,
#                     year_of_business=year_in_bussiness,
#                     # about_company=partnership,
#                     about_company=corporation,
#                     Partnership=redio,
#                     other=other,
#                     tax=tax,
#                 )
#                 users.save()

#                 user.company_profile_status = True
#                 user.save()
#                 messages.success(request, "Company details saved succssfully !!!! ")
#                 return redirect("/login/")
#         except:
#             messages.error(request, "Something WEnt Wrong")
#             return redirect("/profile/company-profile/" + slug)


def employer_detail_list(request, slug):
    # if request.method == "POST":
    #     price = request.POST.get('price')
    #     user = User.objects.get(slug=slug)
    #     user.price = price
    #     user.save()
    users = User.objects.get(slug=slug)
    emp_user = users.id
    print(emp_user, "dddddddddddddddddddddddd")
    try:
        c = CompanyInfo.objects.get(user_id=emp_user)

    except:
        c = None
        messages.error(request, "Please fill company information first")

    userdata = User.objects.all()
    return render(
        request,
        "user/employer/employer-pdf-details.html",
        {"users": users, "userdata": userdata, "c": c},
    )


# Zenerate PDF for Employer
def employer_user_data_pdf(request, slug):
    emp_user = User.objects.get(slug=slug, roll="employer")
    c = CompanyInfo.objects.get(user_id=emp_user.id)
    # print(c.name, c.phone_number, c.fax, c.year_of_business, "fffffffffffffffffffffffffffffffffffffffffffffffffffffff")

    # getting the template
    pdf = html_to_pdf(
        "reports/pdf/employer_details_pdf.html", {"emp_user": emp_user, "c": c}
    )
    # rendering the template
    return HttpResponse(pdf, content_type="application/pdf")


# Adding Employer User data
def emp_add(request):
    userdata = User.objects.all()
    country = Country.objects.all().order_by("name")

    return render(
        request,
        "user/employer/add.html",
        {"userdata": userdata, "country": country},
    )


@permission_required("staff_admin.add_user", raise_exception=True)
@login_required(login_url="/admin/")
def emp_add_userdata(request):
    # try:
    if request.method == "POST":
        gen_pass = generatePassword()
        id = request.POST.get("id")

        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        company_name = request.POST.get("company")
        # latitude = request.POST.get('latitude')
        # longitude = request.POST.get('longitude')

        email = request.POST.get("email")
        mobile_number = request.POST.get("phone")
        address = request.POST.get("address")
        code = mobile_number.split(" ")[0]
        # latitude = request.POST.get('latitude')
        # longitude = request.POST.get('longitude')
        phone = mobile_number.split(" ")[1]

        country = request.POST.get("country")
        city = request.POST.get("city")
        postal = request.POST.get("postal_code")
        user_type = request.POST.get("emp")
        print(user_type, "dddddddddddddddddddddddddddddddddddd")

        print(
            first_name,
            country,
            city,
            postal,
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        )
        df = geopandas.tools.geocode(postal)

        try:
            df["lon"] = df["geometry"].x
            df["lat"] = df["geometry"].y
            lat = df["lat"]
            long = df["lon"]

        except:
            # messages.error(request, "Select valid pin code")
            # return redirect("/admin/employer/add/")
            return JsonResponse(
                {
                    "status": "error",
                    "message": " Please select valid pin code !!!!",
                },
                status=404,
            )

        if User.objects.filter(mobile_number=phone):
            print("qqqqqqqqqqqq")

            return JsonResponse(
                {"status": "error", "message": " Mobile Number allready exits"},
                status=404,
            )

        if user_type == "employer":
            print("hfvbaffgfrg")
            if User.objects.filter(email=email):
                print("rrrrrrrrrrrrr")

                return JsonResponse(
                    {"status": "error", "message": "Email allready exits"},
                    status=404,
                )

            else:
                print("DFFADSJFNADSJFNADSFADSFG")
                userdata = User.objects.create(
                    fname=first_name,
                    lname=last_name,
                    country=country,
                    city=city,
                    post_code=postal,
                    company=company_name,
                    email=email,
                    company_profile_status=False,
                    latitude=lat,
                    longitude=long,
                    password=make_password(gen_pass),
                    mobile_number=phone,
                    country_code=code,
                    address=address,
                    roll=user_type,
                )
                # response = HttpResponse(userdata)
                # response.set_cookie(
                #     userdata, key="userdata", value=userdata.fname, httponly=True
                # )
                # return response

                # set_cookie(userdata , key="jwt", value=fname, httponly=True)
                # userdata.set_cookie("fname", "sfdsfdsfds")

                unique_id = userdata.id + 100
                send_to = [email]
                subject = "Your Password is Here "
                content = (
                    "Hi"
                    + first_name
                    + last_name
                    + "Your UNIQUE ID IS  "
                    + str(unique_id)
                    + " And Your Zenerated Password is  "
                    + gen_pass
                )
                sendMail(subject, content, send_to)
                print("dffffffffffffffffffffff")
                messages.success(
                    request, " Employer User Created and password sent on mail "
                )
                return JsonResponse(
                    {
                        "status": "success",
                        "message": " Employer User Created and password sent on mail !!!!",
                    },
                    status=200,
                )
        else:
            print("dddddddddddddddddddddddddd")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Something went wrong!!!!",
                },
                status=200,
            )
    else:
        return redirect("/admin/employer/")


# return render(request, 'user/employer/add.html')

# except:
#     messages.error(request, "Something Went Wrong")
#     return JsonResponse(
#         {"status": "error", "message": " Please select valid pin code !!!!"},
#         status=404,
#     )


def emp_country_ajax(request):
    country = request.POST.get("select_country")
    state = States.objects.filter(country_id=country).values().order_by("name")

    # nomi = pgeocode.Nominatim('fr')

    if state is None:
        return JsonResponse(
            {
                "status": "error",
                "message": " no changed !!!!",
                "result": "Required state",
            },
            status=200,
        )
    else:

        return JsonResponse(
            {"status": "error", "message": " no changed !!!!", "result": list(state)},
            status=200,
        )


def emp_state_city_ajax(request):
    state = request.POST.get("state_value")

    city = Cities.objects.filter(state_id=state).values()
    # cities = json.dumps(city)

    # print(state.state_code,"dddddddddddddddddddddddddddddddddddddddd")
    # nomi = pgeocode.Nominatim('fr')

    if city is None:
        return JsonResponse(
            {"status": "error", "message": " no changed !!!!"}, status=200
        )
    else:

        return JsonResponse(
            {"status": "error", "message": " no changed !!!!", "result": list(city)},
            status=200,
        )


def emp_postal_code_ajax(request):
    postal_code = request.POST.get("postal_code")

    geolocator = Nominatim(user_agent="geoapiExercises")
    zipcode = postal_code
    location = geolocator.geocode(zipcode)
    nomi = pgeocode.Nominatim("fr")

    return JsonResponse(
        {"status": "error", "message": " no changed !!!!", "location": list(location)},
        status=200,
    )


# Editing Employer data
@login_required(login_url="/admin/")
@permission_required("staff_admin.change_user", raise_exception=True)
def emp_edit_userdata(request, slug):
    try:
        if request.method == "POST":
            slug = request.POST.get("slug")
            first_name = request.POST.get("FName")
            latitude = request.POST.get("latitude")

            longitude = request.POST.get("longitude")
            last_name = request.POST.get("LName")

            company_name = request.POST.get("CName")

            email = request.POST.get("email")

            mobile_number = request.POST.get("phone")
            try:
                phone = mobile_number.split(" ")[1]
            except:
                pass
            country = request.POST.get("country")
            print(country)
            # state = request.POST.get("state")
            # print(state)
            city = request.POST.get("city")
            print(city)
            postal = request.POST.get("Postal_code")
            print(postal)
            address = request.POST.get("address")
            user_type = request.POST.get("emp")
            df = geopandas.tools.geocode(postal)

            try:
                df["lon"] = df["geometry"].x
                df["lat"] = df["geometry"].y
                lat = df["lat"]
                print(lat, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
                long = df["lon"]
                print(long, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

            except:
                messages.error(request, "Select valid pin code")
                return redirect("/admin/employer/edit/" + slug)

            if mobile_number == "" or mobile_number == " " or mobile_number == None:
                userdata = User.objects.filter(slug=slug).update(
                    fname=first_name,
                    country=country,
                    # state=state,
                    city=city,
                    post_code=postal,
                    lname=last_name,
                    address=address,
                    roll=user_type,
                    company=company_name,
                    latitude=lat,
                    longitude=long,
                )
                messages.success(request, " Employer details is updated ")
                return redirect("/admin/employer/")

            phone = mobile_number.split(" ")[1]
            code = mobile_number.split(" ")[0]

            # if latitude == None or longitude == None:
            #     messages.error(request, " Select valid Addresss  ")
            #     return redirect('/admin/employer/edit/' + slug)

            # elif latitude == '' or longitude == '':
            #     messages.error(request, " Select valid Addresss  ")
            #     return redirect('/admin/employer/edit/' + slug)

            try:

                if mobile_number == "" or mobile_number == " " or mobile_number == None:
                    userdata = User.objects.filter(slug=slug).update(
                        fname=first_name,
                        lname=last_name,
                        country=country,
                        # state=state,
                        city=city,
                        post_code=postal,
                        address=address,
                        roll=user_type,
                        company=company_name,
                        latitude=lat,
                        longitude=long,
                    )
                    messages.success(request, " Employer details is updated ")
                    return redirect("/admin/employer/")

                # if User.objects.get(mobile_number=phone):
                #     messages.error(request, "Mobile Number allready taken ")
                #     return redirect('/admin/employer/edit/'+slug)

                else:
                    code = mobile_number.split(" ")[0]
                    phone = mobile_number.split(" ")[1]
                    print("dddddddddddddddddddddddddddd")
                    userdata = User.objects.filter(slug=slug).update(
                        fname=first_name,
                        lname=last_name,
                        country=country,
                        # state=state,
                        city=city,
                        post_code=postal,
                        mobile_number=phone,
                        country_code=code,
                        address=address,
                        roll=user_type,
                        company=company_name,
                        latitude=lat,
                        longitude=long,
                    )
                    messages.success(request, " Employer details is updated ")
                    return redirect("/admin/employer/")
            except:
                code = mobile_number.split(" ")[0]
                phone = mobile_number.split(" ")[1]
                userdata = User.objects.filter(slug=slug).update(
                    fname=first_name,
                    country=country,
                    # state=state,
                    city=city,
                    post_code=postal,
                    mobile_number=phone,
                    lname=last_name,
                    country_code=code,
                    address=address,
                    company=company_name,
                    roll=user_type,
                    latitude=lat,
                    longitude=long,
                )
                messages.success(request, "Employer details is updated ")
                print("dddddddddddddddddddddddddddd")

                return redirect("/admin/employer/")

        else:
            # country = Country.objects.all().order_by("name")
            users = User.objects.filter(slug=slug)
            user = User.objects.get(slug=slug)
            # state = (
            #     States.objects.filter(country_id=user.country_id).values().order_by("name")
            # )
            # city = Cities.objects.filter(state_id=user.state_id).values()
            userdata = User.objects.all()
            return render(
                request,
                "user/employer/edit.html",
                {
                    "users": users,
                    "userdata": userdata,
                },
            )

    except:
        messages.error(request, "Something Went Wrong")
        return redirect("/admin/employer/edit/" + slug)


@login_required(login_url="/admin/")
def emp_search(request):
    if request.method == "GET":
        u = request.GET.get("Q_emp")
        print(u, "fffffffffffffffffffffff")
        emp_user = User.objects.filter(
            Q(fname__icontains=u) | Q(lname__icontains=u) | Q(email__icontains=u),
            soft_del_status=0,
            roll="employer",
        ).order_by("-created_at")
        print(emp_user, "ggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
        page = request.GET.get("page", 1)
        userdata = User.objects.all()
        paginator = Paginator(emp_user, 10)
        try:
            users = paginator.page(page)
            # print(users, "gggggggggggggggggggggggg")

        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(
            request,
            "user/employer/employer.html",
            {"emp_user": emp_user, "users": users, "userdata": userdata},
        )


# Deleting Employer Data
@permission_required("staff_admin.delete_user", raise_exception=True)
@login_required(login_url="/admin/")
def emp_userdata_del(request, id):
    instance = User.objects.get(id=id)
    instance.delete()
    messages.error(request, " Client User is deleted ")
    return redirect("/admin/employer/")


# Display Applicant data
@permission_required("staff_admin.view_user", raise_exception=True)
@login_required(login_url="/admin/")
def applicant_user_data(request):
    app_user = User.objects.filter(roll="applicant", soft_del_status=0).order_by(
        "-created_at"
    )
    userdata = User.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(app_user, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(
        request,
        "user/applicant/applicant.html",
        {"app_user": app_user, "users": users, "userdata": userdata},
    )


# Display View data
def applicant_view_data(request, slug):
    app_user = User.objects.get(slug=slug, roll="applicant")
    userdata = User.objects.all()
    return render(
        request,
        "user/applicant/view.html",
        {"app_user": app_user, "userdata": userdata},
    )


def applicant_detail_list(request, slug):
    # if request.method == "POST":
    #     price = request.POST.get('price')
    #     user = User.objects.get(slug=slug)
    #     user.price = price
    #     user.save()

    users = User.objects.filter(slug=slug)
    u = User.objects.get(slug=slug)
    try:
        data = ApplicantDeatails.objects.get(user_id=u.id)
        print(data.image.url, "dddddddddddddddddddddddddd")
    except:
        data = None
    # print(data.booster_dose, "fffffffffffffffffffffffffff")
    job = Category.objects.all()
    userdata = User.objects.all()
    training = Training.objects.all()
    return render(
        request,
        "user/applicant/applicant-pdf-details.html",
        {
            "users": users,
            "job": job,
            "userdata": userdata,
            "training": training,
            "data": data,
        },
    )


# Appicant details In PDF
def applicant_user_data_pdf(request, slug):
    app_user = User.objects.get(slug=slug, roll="applicant")
    # try:
    data = ApplicantDeatails.objects.get(user_id=app_user.id)
    # print(data,"ddddddddddddddddddddddd")
    if data:
        pdf = html_to_pdf(
            "reports/pdf/applicant_details_pdf.html",
            {"app_user": app_user, "data": data},
        )
        return HttpResponse(pdf, content_type="application/pdf")
    else:
        pdf = html_to_pdf(
            "reports/pdf/applicant_details_pdf.html", {"app_user": app_user}
        )
        return HttpResponse(pdf, content_type="application/pdf")
    # except:
    #     messages.error(request,"nooooooooooooo")
    #     pdf = html_to_pdf('reports/pdf/applicant_details_pdf.html',
    #                         {'app_user': app_user})
    #     return HttpResponse(pdf, content_type='application/pdf')

    # return HttpResponse(pdf, content_type='application/pdf')

    # return render(request, 'reports/pdf/applicant_details_pdf.html', {'app_user': app_user, 'data': datas})

    # print(data.booster_dose,"ffffffffffffffffffffffffff")
    # for i  in app_user:
    #     print()
    # getting the template
    # pdf = html_to_pdf('reports/pdf/applicant_details_pdf.html',
    #                   {'app_user': app_user, 'data': data})
    # rendering the template


# Appicant DATA In PDF


def applicant_data_pdf(request, slug):

    if request.method == "POST":
        id = request.POST.get("ids")
        print(id, "gggggggggggggggggggggggggg")
        price = request.POST.get("price")
        Vaccination = request.POST.get("Vaccination")
        print(Vaccination, "ddddddddddddddddddddddddddddddddddddd")
        image = request.POST.get("img")
        print(image, "fffffffffffffffff")
        booster_dose = request.POST.get("booster_dose")
        # city = request.POST.get("city")
        dob = request.POST.get("dob")
        # position = request.POST.get("position")
        nmc_pin = request.POST.get("nmc_pin")
        flexCheck = request.POST.get("flexCheck")
        Enhance_DBC_No = request.POST.get("Enhance_DBC_No")
        Yes_Recitations = request.POST.get("Yes_Recitations")
        DBC_Issues_Date = request.POST.get("DBC_Issues_Date")
        DBC_Status = request.POST.get("DBC_Status")
        Work_Checkes = request.POST.get("Work_Checkes")
        Emergency = request.POST.get("Emergency")
        training = request.POST.get("training")
        training_start = request.POST.get("training_start")
        training_end = request.POST.get("training_end")
        users = User.objects.get(slug=slug)
        # fs = FileSystemStorage()
        # filename = fs.save(image.name, image)
        # print(filename, "dddddddddddddddddddddddd")
        obj = User.objects.get(slug=slug)
        print(obj, "ffffffffffffffffff")
        obj.price = price
        obj.save()
        data = ApplicantDeatails.objects.filter(user_id=id)
        if data:
            data = ApplicantDeatails.objects.filter(user_id=id).update(
                user_id=users.id,
                vaccinated=Vaccination,
                booster_dose=booster_dose,
                image=image,
                dob=dob,
                Mnc_pin=nmc_pin,
                recitation=flexCheck,
                enhance_dbc=Enhance_DBC_No,
                recitation_desc=Yes_Recitations,
                enhance_dbc_issue=DBC_Issues_Date,
                dbc_status=DBC_Status,
                work_checkes=Work_Checkes,
                emergency_no=Emergency,
                training_id=training,
                training_start_date=training_start,
                training_end_date=training_end,
                vaccination_status=True,
            )
        else:

            data = ApplicantDeatails.objects.create(
                user_id=users.id,
                vaccinated=Vaccination,
                booster_dose=booster_dose,
                image=image,
                dob=dob,
                Mnc_pin=nmc_pin,
                recitation=flexCheck,
                enhance_dbc=Enhance_DBC_No,
                recitation_desc=Yes_Recitations,
                enhance_dbc_issue=DBC_Issues_Date,
                dbc_status=DBC_Status,
                work_checkes=Work_Checkes,
                emergency_no=Emergency,
                training_id=training,
                training_start_date=training_start,
                training_end_date=training_end,
                vaccination_status=True,
            )
            return JsonResponse(
                {"status": "Success", "message": " Details  updated  !!!!"}, status=200
            )

        # messages.success(request, "doneeeeeeeeeee")
        return JsonResponse(
            {"status": "Success", "message": " Details  Saved  !!!!"}, status=200
        )

    return JsonResponse({"status": "error", "message": "  NO changed !!!!"})


# Adding Employer User data
def app_add(request):
    userdata = User.objects.all()
    country = Country.objects.all()
    job_postion = Category.objects.filter(status=1, soft_del_status=0)
    year = list(range(0, 15))
    month = list(range(0, 13))
    year_list = []
    month_list = []
    for i in year:
        year_list.append(i)
    for i in month:
        month_list.append(i)
    return render(
        request,
        "user/applicant/add.html",
        {
            "userdata": userdata,
            "year_list": year_list,
            "month_list": month_list,
            "country": country,
            "job_postion": job_postion,
        },
    )


@permission_required("staff_admin.add_user", raise_exception=True)
@login_required(login_url="/admin/")
def app_add_userdata(request):
    try:
        # mob = []
        if request.method == "POST":
            gen_pass = generatePassword()
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            email = request.POST.get("email")
            mobile_number = request.POST.get("phone")
            address = request.POST.get("address")
            code = mobile_number.split(" ")[0]
            # latitude = request.POST.get('latitude')
            # longitude = request.POST.get('longitude')

            phone = mobile_number.split(" ")[1]
            # print(code, "sssssssssssssssssssssssssssssssssssssssss")
            country = request.POST.get("country")
            # state = request.POST.get("state")
            city = request.POST.get("city")
            postal = request.POST.get("postal_code")
            job_position = request.POST.get("job")
            exp_year = request.POST.get("exp_year")
            exp_month = request.POST.get("exp_month")

            print(country, city, postal, "gggggggggggggggggggggggggggggggggggggggg")
            user_type = request.POST.get("app")
            df = geopandas.tools.geocode(postal)

            try:
                df["lon"] = df["geometry"].x
                df["lat"] = df["geometry"].y
                lat = df["lat"]
                print(lat, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
                long = df["lon"]
                print(long, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

            except:
                messages.error(request, "Select valid pin code")
                return JsonResponse(
                    {
                        "status": "error",
                        "message": " Please select valid pin code !!!!",
                    },
                    status=404,
                )

            if User.objects.filter(mobile_number=phone):
                messages.error(request, "Mobile Number allready exits")
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Mobile Number allready exits !!!!",
                    },
                    status=404,
                )

            if user_type == "applicant":

                if User.objects.filter(email=email):
                    messages.error(request, "Email allready exits")
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Email allready exits !!!!",
                        },
                        status=404,
                    )
                # if latitude == '' or longitude == '':
                #     messages.error(request, 'Please Select Valid Address')
                #     return redirect('/admin/applicant/add/')
                else:
                    userdata = User.objects.create(
                        fname=first_name,
                        latitude=lat,
                        country=country,
                        # state=state,
                        city=city,
                        post_code=postal,
                        exp_year=exp_year,
                        exp_month=exp_month,
                        company_profile_status=False,
                        longitude=long,
                        lname=last_name,
                        email=email,
                        password=make_password(gen_pass),
                        position_id=job_position,
                        mobile_number=phone,
                        country_code=code,
                        address=address,
                        roll=user_type,
                    )
                    unique_id = userdata.id + 100
                    send_to = [email]
                    subject = "Your Password is Here "
                    content = (
                        "Hi"
                        + first_name
                        + last_name
                        + "Your UNIQUE ID IS  "
                        + str(unique_id)
                        + " And Your Zenerated Password is  "
                        + gen_pass
                    )
                    sendMail(subject, content, send_to)
                    messages.success(
                        request, "Applicant User Created and password sent on mail"
                    )

                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Applicant User Created and password sent on mail  !!!!",
                        },
                        status=200,
                    )
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Something went wrong  !!!!",
                },
                status=200,
            )
    except:
        return JsonResponse(
            {
                "status": "success",
                "message": "Something went wrong  !!!!",
            },
            status=200,
        )


def app_job_position_ajax(request):
    job = request.POST.get("job_position")
    return JsonResponse({"status": "okay", "message": "  changed !!!!"})


# Editing Applicant data
@permission_required("staff_admin.change_user", raise_exception=True)
@login_required(login_url="/admin/")
def app_edit_userdata(request, slug):
    try:
        if request.method == "POST":
            slug = request.POST.get("slug")

            first_name = request.POST.get("FName")

            last_name = request.POST.get("LName")
            email = request.POST.get("email")
            mobile_number = request.POST.get("phone")
            address = request.POST.get("address")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            print(latitude, longitude, "fffffffffffffffffffffff")
            country = request.POST.get("country")
            # state = request.POST.get("state")
            city = request.POST.get("city")
            postal = request.POST.get("Postal_code")
            user_type = request.POST.get("app")
            print(user_type, "gggggggggggggggggggggggggggggggggggggggggg")
            job_position = request.POST.get("job")
            exp_year = request.POST.get("year")
            exp_month = request.POST.get("month")
            print(
                country,
                # state,
                city,
                postal,
                exp_year,
                exp_month,
                "ffffffffffffffffffffffffff",
            )
            df = geopandas.tools.geocode(postal)

            try:
                df["lon"] = df["geometry"].x
                df["lat"] = df["geometry"].y
                lat = df["lat"]
                print(lat, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
                long = df["lon"]
                print(long, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

            except:
                messages.error(request, "Select valid pin code")
                return redirect("/admin/applicant/edit/" + slug)

            if mobile_number == "" or mobile_number == " " or mobile_number == None:
                userdata = User.objects.filter(slug=slug).update(
                    fname=first_name,
                    lname=last_name,
                    address=address,
                    country=country,
                    # state=state,
                    city=city,
                    post_code=postal,
                    exp_year=exp_year,
                    exp_month=exp_month,
                    latitude=lat,
                    longitude=long,
                    roll=user_type,
                    position_id=job_position,
                )
                messages.success(request, " Applicant details is updated ")
                print("sdajsbcjsbhujsb")
                return redirect("/admin/applicant/")

            phone = mobile_number.split(" ")[1]
            code = mobile_number.split(" ")[0]
            # if latitude == '' or longitude == '':

            #     messages.error(request, 'Please Select Valid Address')
            #     return redirect('/admin/applicant/edit/' + slug)

            # elif latitude == None or longitude == None:
            #     messages.error(request, " Select valid Addresss  ")
            #     return redirect('/admin/applicant/edit/' + slug)

            try:
                if mobile_number == "" or mobile_number == " " or mobile_number == None:

                    userdata = User.objects.filter(slug=slug).update(
                        fname=first_name,
                        lname=last_name,
                        address=address,
                        country=country,
                        state=state,
                        city=city,
                        post_code=postal,
                        exp_year=exp_year,
                        exp_month=exp_month,
                        latitude=lat,
                        longitude=long,
                        roll=user_type,
                        position_id=job_position,
                    )
                    messages.success(request, " Applicant details is updated ")
                    print("ttttttttttttttttttttttttt")

                    return redirect("/admin/applicant/")

                if User.objects.get(mobile_number=phone):
                    messages.error(request, "Mobile Number allready taken ")
                    return redirect("/admin/applicant/edit/" + slug)
                else:
                    code = mobile_number.split(" ")[0]
                    phone = mobile_number.split(" ")[1]
                    userdata = User.objects.filter(slug=slug).update(
                        fname=first_name,
                        lname=last_name,
                        mobile_number=phone,
                        country_code=code,
                        country=country,
                        state=state,
                        city=city,
                        post_code=postal,
                        exp_year=exp_year,
                        exp_month=exp_month,
                        latitude=lat,
                        longitude=long,
                        position_id=job_position,
                        address=address,
                        roll=user_type,
                    )
                    messages.success(request, " Applicant details is updated ")
                    print("fffffffffffffffffffffffffffffff")

                    return redirect("/admin/applicant/")
            except:
                userdata = User.objects.filter(slug=slug).update(
                    fname=first_name,
                    lname=last_name,
                    mobile_number=phone,
                    country_code=code,
                    country=country,
                    state=state,
                    city=city,
                    post_code=postal,
                    exp_year=exp_year,
                    exp_month=exp_month,
                    latitude=lat,
                    longitude=long,
                    position_id=job_position,
                    address=address,
                    roll=user_type,
                )
                print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

                messages.success(request, "Applicant details is updated ")
                return redirect("/admin/applicant/edit/" + slug)
        else:
            userdata = User.objects.all()
            # country = Country.objects.all()
            users = User.objects.get(slug=slug)

            user = User.objects.get(slug=slug)
            job = Category.objects.all()
            # state = States.objects.filter(country_id=user.country_id).values()
            # city = Cities.objects.filter(state_id=user.state_id).values()
            year = list(range(0, 15))
            month = list(range(0, 13))
            year_list = []
            month_list = []
            for i in year:
                year_list.append(i)

            for i in month:
                month_list.append(i)
            years = int(users.exp_year)
            months = int(users.exp_month)

            return render(
                request,
                "user/applicant/edit.html",
                {
                    "month_list": month_list,
                    "year_list": year_list,
                    "years": years,
                    "months": months,
                    "users": users,
                    "job": job,
                    "userdata": userdata,
                },
            )

    except:

        messages.success(request, "Something went wrong")
        return redirect("/admin/applicant/")


@login_required(login_url="/admin/")
def app_search(request):
    # try:
    if request.method == "GET":
        u = request.GET.get("Q_app", None)
        if not u:
            u = ""
        app_user = User.objects.filter(
            Q(fname__icontains=u) | Q(lname__icontains=u) | Q(email__icontains=u),
            soft_del_status=0,
            roll="applicant",
        ).order_by("-created_at")
        page = request.GET.get("page", 1)
        userdata = User.objects.all()
        paginator = Paginator(app_user, 10)
        try:
            users = paginator.page(page)
            print(users, "gggggggggggggggggggggggg")

        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(
            request,
            "user/applicant/applicant.html",
            {" userdata ": userdata, "users": users, "app_user": app_user},
        )


# except:
#     messages.error(request, "SomeThing Went wrong")
#     userdata = User.objects.all()
#     return render(request, 'user/applicant/applicant.html', {' userdata ': userdata})

# Deleting Applicant Data


@permission_required("staff_admin.delete_user", raise_exception=True)
@login_required(login_url="/admin/")
def app_userdata_del(request, id):
    instance = User.objects.get(id=id)
    instance.soft_delete()
    messages.error(request, " Applicant User is deleted ")
    return redirect("/admin/applicant/")


# def applicat_details_pdf(request):

#     pdf = html_to_pdf('app_pdf.html', {'count_app': count_app})
#     # rendering the template
#     return HttpResponse(pdf, content_type='application/pdf')


@permission_required("staff_admin.view_job_category", raise_exception=True)
def category(request):
    cat = Category.objects.filter(soft_del_status=0).order_by("-create_at")
    cat_list = []
    for i in cat:
        x_dict = {"obj": i}

        x = i.leave_day
        z = i.DAY_CHOISE
        y = json.loads(x)
        l = list()
        c = 0
        for i in z:
            if z[c][0] in y:
                l.append(z[c][1])
            else:
                pass
            c += 1
        x_dict["leave"] = l
        cat_list.append(x_dict)

    userdata = User.objects.all()
    return render(
        request,
        "job_category/category.html",
        {"cat": cat, "userdata": userdata, "cat_list": cat_list},
    )


@permission_required("staff_admin.add_job_category", raise_exception=True)
def add_category(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            week_hour = request.POST.get("Week")
            leave_day = request.POST.getlist("Leave[]")
            shift_diffrence = request.POST.get("Shift")

            status = request.POST.get("status")
            z = json.dumps(leave_day)
            cat = Category.objects.create(
                name=name,
                week_hour=week_hour,
                leave_day=z,
                shift_diffrence=shift_diffrence,
                status=status,
            )

            messages.success(request, "Successfully ! Job Category Created")
            return redirect("/admin/category/")
        else:
            userdata = User.objects.all()
            u = Category.DAY_CHOISE

            return render(
                request, "job_category/add.html", {"userdata": userdata, "u": u}
            )
    except:
        messages.success(request, "Something Went Wrong")
        return redirect("/admin/category/")


@permission_required("staff_admin.edit_job_category", raise_exception=True)
def edit_category(request, slug):
    try:
        if request.method == "POST":
            id = request.POST.get("id")
            name = request.POST.get("name")
            week_hour = request.POST.get("Week")
            leave_day = request.POST.getlist("Leave[]")
            shift_diffrence = request.POST.get("Shift")

            leave = json.dumps(leave_day)

            status = request.POST.get("status")

            cat = Category.objects.filter(slug=slug).update(
                name=name,
                week_hour=week_hour,
                leave_day=leave,
                shift_diffrence=shift_diffrence,
                status=status,
            )

            messages.success(request, "Successfully ! Job Category Updated")
            return redirect("/admin/category/")
        else:
            userdata = User.objects.all()
            cat = Category.objects.get(slug=slug)

            u = Category.DAY_CHOISE

            x = json.loads(cat.leave_day)

            return render(
                request,
                "job_category/edit.html",
                {"userdata": userdata, "days": u, "select_day": x, "cat": cat},
            )
    except:
        messages.success(request, "Something Went Wrong ")
        return redirect("/admin/category/")


@permission_required("staff_admin.delete_job_category", raise_exception=True)
def del_category(request, id):
    cat = Category.objects.get(id=id)
    user = User.objects.filter(position_id=cat.id)
    if user:
        messages.error(request, "You couldn't delete the Category")
        return redirect("/admin/category/")

    cat.soft_delete()
    messages.error(request, "Successfully ! Job Category Deleted")
    return redirect("/admin/category/")


# Searching UserData from User Database


# Update Admin Profile
@login_required(login_url="/admin/")
def myprofile(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        image = request.FILES.get("img")
        u = User.objects.get(id=id)
        if u.is_superuser:
            try:
                if image is None:
                    userdata = User.objects.get(id=id)
                    userdata.username = username
                    userdata.email = email
                    userdata.save()
                    messages.success(
                        request, "Successfully ! Profile Details is Updated "
                    )
                    return redirect("/admin/myprofile/" + id)

                else:

                    userdata = User.objects.get(id=id)
                    user = userdata.image
                    user.delete()
                    userdata.username = username
                    userdata.email = email
                    userdata.image = image
                    userdata.save()
                    messages.success(
                        request, "Successfully ! Profile Details is Updated"
                    )
                    return redirect("/admin/myprofile/" + id)
            except:
                messages.error(request, " Email allready register ")
                return redirect("/admin/myprofile/" + id)

        elif u.roll == "Subadmin":
            try:
                if image is None:
                    userdata = User.objects.get(id=id)
                    userdata.username = username
                    userdata.email = email
                    userdata.save()
                    messages.success(
                        request, "Successfully ! Profile Details is Updated"
                    )
                    return redirect("/admin/myprofile/" + id)

                else:

                    userdata = User.objects.get(id=id)
                    user = userdata.image
                    userdata.username = username
                    userdata.email = email
                    user.delete()
                    userdata.image = image
                    userdata.save()
                    messages.success(
                        request, "Successfully ! Profile Details is Updated"
                    )
                    return redirect("/admin/myprofile/" + id)

            except:
                messages.error(request, " Email allready register ")
                return redirect("/admin/myprofile/" + id)

    else:
        userdata = User.objects.all()
        u = User.objects.get(id=id)
        return render(
            request, "admin_profile/myprofile.html", {"userdata": userdata, "u": u}
        )


# Changing Password from admin
@login_required(login_url="/admin/")
def change_password(request):
    try:
        if request.method == "POST":
            Cpwd = request.POST.get("Cpwd")
            Npwd = request.POST.get("Npwd")
            user = User.objects.get(id=request.user.id)
            un = user.username
            check = user.check_password(Cpwd)
            if check == True:
                user.set_password(Npwd)
                user.save()
                user = User.objects.get(username=un)
                login_check(request, user)
                messages.success(request, " Password changed Successfully !!!! ")
                return redirect("/admin/change_password/")
            else:
                messages.error(request, " Old Password is Wrong ")
                return redirect("/admin/change_password/")
        else:
            user = User.objects.get(id=request.user.id)
            userdata = User.objects.all()
            return render(
                request,
                "admin_profile/change_password.html",
                {"user": user, "userdata": userdata},
            )
    except:
        messages.error(request, "Something Went Wrong")
        return redirect("/admin/change_password/")


# Forgotpassword via link on gmail
def forgotpassword(request):

    try:
        if request.method == "POST":
            email = request.POST.get("Email")

            e = email_templates.objects.get(id=1)

            u = User.objects.get(email=email)

            if u.is_superuser:
                o = generateOTP()
                us = hash(o)
                currnt_time = datetime.now()

                u.OTP_string = us
                u.reset_time_link = str(currnt_time)

                u.save()

                send_to = [email]
                subject = e.sub
                print(subject)

                content = e.content
                print(content)
                a = request.build_absolute_uri()

                url = a + "forgotpasswordform/" + str(us)
                t = strip_tags(content)
                c = t.replace("{name}", u.username)
                msg = c.replace("{LINK}", url)

                sendMail(subject, msg, send_to)

                messages.success(request, " 'Successfully ! Link send on your mail")
                return redirect("/admin/forgotpassword/")
            elif u:

                messages.error(request, "Email is not exist")

                return redirect("/admin/forgotpassword/")
    except:
        messages.error(request, "Email is not exist")
        return redirect("/admin/forgotpassword/")

    return render(request, "admin_profile/forgot_password.html")


# Change Forgot Password form
def forgot_password_form(request, slug):
    if request.method == "POST":
        slug = request.POST.get("us")
        email = request.POST.get("email")
        reset_time = request.POST.get("reset_time")

        o = request.POST.get("newpassword")
        u = request.POST.get("confirmpassword")
        if o == u:
            u = User.objects.filter(email=email, OTP_string=slug).update(
                password=make_password(o)
            )
            messages.success(request, "Successfully ! Password Changed ")
            remove = User.objects.filter(email=email, OTP_string=slug).update(
                OTP_string=None
            )
            return redirect("/admin/")
        else:
            messages.error(request, "Password does not match")
            return redirect("/admin/forgot_password_form/" + slug)
    else:
        try:
            u = User.objects.get(OTP_string=slug)
            if u is None:
                pass
        except:
            return HttpResponse(
                ' <h1 style="margin-left:100px  " > Sorry Link is valid only one time</h1> <br> <button style="margin-left:100px "  class="btn btn-success" ><a class="btn btn-success" href="/admin/"> back to login</a></button>'
            )
        userdata = User.objects.all()
        return render(
            request, "admin_profile/forgot_password_form.html", {"userdata": userdata}
        )


# Display Pages from pages model


@login_required(login_url="/admin/")
@permission_required("staff_admin.view_pages", raise_exception=True)
def Cms_Pages(request):
    terms = pages.objects.all()
    userdata = User.objects.all()
    return render(
        request,
        "cms_pages/pages/cms_pages.html",
        {"terms": terms, "userdata": userdata},
    )


# Add Pages from pages model


@login_required(login_url="/admin/")
@permission_required("staff_admin.add_pages", raise_exception=True)
def add_Cms_Pages(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("editor")
        data = pages.objects.create(title=title, content=content)
        data.save()
        messages.success(request, "CMS Pages is added ")
        return redirect("/admin/Cms_Pages/")
    terms = pages.objects.all()
    userdata = User.objects.all()
    return render(
        request, "cms_pages/pages/add.html", {"terms": terms, "userdata": userdata}
    )


# Edit Pages from pages model


@login_required(login_url="/admin/")
@permission_required("staff_admin.change_pages", raise_exception=True)
def edit_Cms_Pages(request, slug):
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            text = request.POST.get("text")
            content = request.POST.get("editor")
            img2 = request.FILES.get("img2")

            if content is " ".strip():
                messages.error(request, "content required")
                return redirect("/admin/Cms_Pages/" + slug)
            elif img2 is None:

                messages.success(request, "Pages is updated ")
                data = pages.objects.filter(slug=slug).update(
                    title=title, content=content
                )
                return redirect("/admin/Cms_Pages")

            elif img2:
                fs = FileSystemStorage()
                filename = fs.save(img2.name, img2)
                messages.success(request, "Pages is updated ")
                data = pages.objects.filter(slug=slug).update(
                    title=title, image=img2, content=content
                )
                return redirect("/admin/Cms_Pages")
            elif text:
                messages.success(request, "Pages is updated ")
                data = pages.objects.filter(slug=slug).update(
                    title=title, image=img2, text=text, content=content
                )
                return redirect("/admin/Cms_Pages")

        else:
            terms = pages.objects.get(slug=slug)
            userdata = User.objects.all()
            return render(
                request,
                "cms_pages/pages/edit.html",
                {"terms": terms, "userdata": userdata},
            )
    except:
        messages.error(request, "Something Went wrong ")
        return redirect("/admin/edit_Cms_Pages/" + slug)


# if image is None:
#                     userdata = User.objects.get(id=id)
#                     userdata.username = username
#                     userdata.email = email
#                     userdata.save()
#                     messages.success(request, " Profile details is updated ")
#                     return redirect('/admin/myprofile/' + id)


#                 else:

#                     userdata = User.objects.get(id=id)
#                     user = userdata.image
#                     userdata.username = username
#                     userdata.email = email
#                     user.delete()
#                     userdata.image = image
#                     userdata.save()
#                     messages.success(request, " Profile details is updated ")
#                     return redirect('/admin/myprofile/' + id)


# Delete Pages from pages model


@login_required(login_url="/admin/")
@permission_required("staff_admin.delete_pages", raise_exception=True)
def delete_Cms_Pages(request, slug):
    instance = pages.objects.get(slug=slug)
    instance.soft_delete()
    messages.error(request, " deleted ")
    return redirect("/admin/Cms_Pages/")


# Display Email_tem from email model
# @permission_required('user.Subadmin')
@permission_required("staff_admin.view_email_templates", raise_exception=True)
@login_required(login_url="/admin/")
def Email_tem(request):
    email = email_templates.objects.all()
    userdata = User.objects.all()
    return render(
        request, "cms_pages/email/email.html", {"email": email, "userdata": userdata}
    )


#  Add_email from email model


@login_required(login_url="/admin/")
@permission_required("staff_admin.add_email_templates", raise_exception=True)
def add_email(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            sub = request.POST.get("subject")
            content = request.POST.get("content")
            email = email_templates.objects.create(name=name, sub=sub, content=content)
            email.save()
            messages.success(request, "Email Templates is Created ")
            return redirect("/admin/email")
        return render(request, "cms_pages/email/add.html")
    except:
        messages.error(request, "Something Went Wrong")
        return redirect("/admin/email")


#  Edit_email from email model


@login_required(login_url="/admin/")
@permission_required("staff_admin.change_email_templates", raise_exception=True)
def edit_email(request, slug):
    try:
        if request.method == "POST":
            id = request.POST.get("id")
            name = request.POST.get("name")
            sub = request.POST.get("subject")
            content = request.POST.get("content")
            email = email_templates.objects.filter(slug=slug).update(
                name=name, sub=sub, content=content
            )
            messages.success(request, "Successfully !  Updated Email Templates")
            return redirect("/admin/email")

        email = email_templates.objects.filter(slug=slug)
        userdata = User.objects.all()
        return render(
            request, "cms_pages/email/edit.html", {"email": email, "userdata": userdata}
        )
    except:
        messages.error(request, "Something Went Wrong")
        return redirect("/admin/email")


#  del_email_tem from email model


@permission_required("staff_admin.delete_email_templates", raise_exception=True)
@login_required(login_url="/admin/")
def del_email_tem(request, id):
    email = email_templates.objects.get(id=id)
    email.soft_delete()
    messages.error(request, "Email Templates is delete ")
    return redirect("/admin/email/")


# Display global_setting from email model

# @permission_required('staff_admin.view_global_setting', raise_exception=True)
# @login_required(login_url='/admin/')
# def global_setting(request):
#     e = Global_setting.objects.filter(soft_del_status=0)
#     userdata = User.objects.all()
#     return render(request, 'cms_pages/global/global.html', {'userdata': userdata, 'e': e})


# Add global_setting from email model
# @login_required(login_url='/admin/')
# @permission_required('staff_admin.add_global_setting', raise_exception=True)
# def add_global_setting(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         img = request.FILES.get('image')
#         print(img,"ffffffffffffffffffffff")
#         facebook_link = request.POST.get('facebook')
#         instagram_link = request.POST.get('instagram')
#         twitter_link = request.POST.get('pintrest')

#         pintrest_link = request.POST.get('pintrest')
#         linkdin_link = request.POST.get('linkdin')
#         details = request.POST.get('editor')

#         if Global_setting.objects.filter(email=email).exists():
#             messages.error(request, 'email allready')
#             return redirect('/admin/global/add')
#         else:
#             fs = FileSystemStorage()
#             filename = fs.save(img.name, img)
#             global_setting = Global_setting.objects.create(name=name, twitter_link=twitter_link, email=email, img=filename,
#                                                            facebook_link=facebook_link,
#                                                            instagram_link=instagram_link, pintrest_link=pintrest_link,
#                                                            linkdin_link=linkdin_link, discripion=details)
#             global_setting.save()
#             messages.success(request, 'global setting Templates is Created ')

#             return redirect('/admin/global')
#     userdata = User.objects.all()
#     return render(request, 'cms_pages/global/add.html', {'userdata': userdata})


# Edit global_setting from email model
@login_required(login_url="/admin/")
@permission_required("staff_admin.change_global_setting", raise_exception=True)
def edit_global_setting(request, slug):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        img = request.FILES.get("image")
        facebook_link = request.POST.get("facebook")
        instagram_link = request.POST.get("instagram")
        twitter_link = request.POST.get("pintrest")

        pintrest_link = request.POST.get("pintrest")
        linkdin_link = request.POST.get("linkdin")
        details = request.POST.get("editor")
        try:
            if img is None:

                global_setting = Global_setting.objects.filter(slug=slug).update(
                    name=name,
                    email=email,
                    twitter_link=twitter_link,
                    facebook_link=facebook_link,
                    instagram_link=instagram_link,
                    pintrest_link=pintrest_link,
                    linkdin_link=linkdin_link,
                    discripion=details,
                )

                messages.success(request, "Successfully ! Updated Data")
                return redirect("/admin/global/edit/" + slug)
            else:
                fs = FileSystemStorage()
                filename = fs.save(img.name, img)
                global_setting = Global_setting.objects.filter(slug=slug).update(
                    name=name,
                    img=filename,
                    twitter_link=twitter_link,
                    email=email,
                    facebook_link=facebook_link,
                    instagram_link=instagram_link,
                    pintrest_link=pintrest_link,
                    linkdin_link=linkdin_link,
                    discripion=details,
                )

                messages.success(request, "Successfully ! Updated Data")
                return redirect("/admin/global/edit/" + slug)
        except:
            messages.error(request, "Something Went Wrong")
            return redirect("/admin/global/edit/" + slug)

    userdata = User.objects.all()
    try:
        global_setting = Global_setting.objects.get(slug=slug)
    except:
        global_setting = None
    return render(
        request,
        "cms_pages/global/edit.html",
        {"userdata": userdata, "global_setting": global_setting},
    )


# Delete global_setting from email model
# @login_required(login_url='/admin/')
# @permission_required('staff_admin.delete_global_setting', raise_exception=True)

# def del_global_setting(request, slug):
#     global_setting = Global_setting.objects.get(slug=slug)
#     global_setting.soft_delete()
#     messages.error(request, 'global setting is delete ')
#     return redirect('/admin/global/')


# Qr Code Zenerate
@permission_required("staff_admin.view_qr_code", raise_exception=True)
def qr_code(request):
    if request.method == "POST":
        Qr_url = request.POST.get("name")
        QR_save = Qr_Code.objects.create(Qr_url=Qr_url)
        messages.success(request, "wahhhhhhhhh bate ")
        return redirect("/admin/qr_code")
    else:
        qr_code = Qr_Code.objects.all()
        return render(request, "base/qr_code.html", {"qrcode": qr_code})


# Delete Qr Code
@permission_required("staff_admin.delete_qr_code", raise_exception=True)
def delete_qr(request, id):
    qr = Qr_Code.objects.get(id=id)
    qr.delete()
    messages.error(request, "very bad bate ")
    return redirect("/admin/qr_code")


#  ChatProcess Code
@permission_required("staff_admin.delete_qr_code", raise_exception=True)
@login_required(login_url="/admin/")
def chat_view(request):
    users = []
    chat_with = ""
    if request.user.roll == "applicant":
        users = User.objects.filter(roll="admin")
        chat_with = "Admin"
    if request.user.roll == "employer":
        users = User.objects.filter(roll="admin")
        chat_with = "Admin"
    if request.user.roll == "admin":
        users = User.objects.filter(Q(roll="applicant") | Q(roll="employer"))
        chat_with = "Applicant or Employer"
    threads = (
        Thread.objects.by_user(user=request.user)
        .prefetch_related("chatmessage_thread")
        .order_by("timestamp")
    )
    userdata = User.objects.all()

    context = {
        "threads": threads,
        "users": users,
        "chat_with": chat_with,
        "userdata": userdata,
    }
    return render(
        request,
        "chat.html",
        context,
    )


# Sending message via Ajax
def chat_ajax(request):
    if request.method == "POST":
        data = request.POST.get("select")
        return JsonResponse(
            {"status": "success", "message": "Status changed successfully !!!!"},
            status=200,
        )
    return JsonResponse(
        {"status": "error", "message": "NO Status changed successfully !!!!"},
        status=404,
    )


# Display Reports
def reports_list(request):
    userdata = User.objects.all()
    count_emp = User.objects.filter(soft_del_status=0, roll="employer").count()

    count_app = User.objects.filter(soft_del_status=0, roll="applicant").count()

    return render(
        request,
        "reports/reports.html",
        {"count_emp": count_emp, "count_app": count_app, "userdata": userdata},
    )


# Zenerate Employee PDF
def emp_pdf(request):
    count_emp = User.objects.filter(soft_del_status=0, roll="employer").count()
    # getting the template
    all_emp = User.objects.filter(soft_del_status=0, roll="employer").values()

    pdf = html_to_pdf(
        "reports/pdf/emp_pdf.html", {"count_emp": count_emp, "all_emp": all_emp}
    )

    # rendering the template
    return HttpResponse(pdf, content_type="application/pdf")


# Zenerate Applicant PDF
def app_pdf(request):
    count_app = User.objects.filter(soft_del_status=0, roll="applicant").count()
    all_app = User.objects.filter(soft_del_status=0, roll="applicant").values()
    # getting the template
    pdf = html_to_pdf(
        "reports/pdf/app_pdf.html", {"count_app": count_app, "all_app": all_app}
    )
    # rendering the template
    return HttpResponse(pdf, content_type="application/pdf")


@permission_required("staff_admin.view_training", raise_exception=True)
# Display Training Managment
def training(request):
    trainings = Training.objects.filter(soft_del_status=0).order_by("-timestamp")
    userdata = User.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(trainings, 5)
    try:
        users_training = paginator.page(page)
    except PageNotAnInteger:
        users_training = paginator.page(1)
    except EmptyPage:
        users_training = paginator.page(paginator.num_pages)
    return render(
        request,
        "training/training.html",
        {"training": trainings, "users_training": users_training, "userdata": userdata},
    )


# Add Training Managment
@login_required(login_url="/admin/")
def add_training(request):
    try:
        if request.method == "POST":
            training_name = request.POST.get("training_name")
            user = request.POST.getlist("training-user[]")

            status = request.POST.get("status")

            training = Training.objects.create(
                training_name=training_name, Status=status
            )
            for i in user:
                training.user.add(int(i))
                training.save()
            messages.success(request, "Successfully ! Training is added")
            return redirect("/admin/training")
        else:
            userdata = User.objects.all()
            return render(request, "training/add.html", {"userdata": userdata})
    except:
        messages.error(request, "Training is not added ")
        return redirect("/admin/add")


# Edit Training Managment


@login_required(login_url="/admin/")
def edit_training(request, id):

    try:
        obj = Training.objects.get(id=id)
        l = obj.user.all()
        if request.method == "POST":

            training_name = request.POST.get("training_name")
            status = request.POST.get("status")
            userlist = request.POST.getlist("userlist[]")

            if training_name and status:
                obj.training_name = training_name
                obj.Status = status
                obj.save()
            if userlist:
                obj.user.set(userlist)
                obj.save()
            userdata = User.objects.all()
            messages.success(request, "Successfully ! Training is Updated ")
            return redirect("/admin/training")
        else:
            obj = Training.objects.get(id=id)
            l = obj.user.all()
            user_list = []
            for i in l:
                user_list.append(i.id)

            userdata = User.objects.all()

            return render(
                request,
                "training/edit.html",
                {
                    "old_data": l,
                    "obj": obj,
                    "user_list": user_list,
                    "userdata": userdata,
                },
            )
    except:
        messages.error(request, "Training is not update")
        return redirect("/admin/edit")


# @login_required
def social(request):
    # user = social_user.objects.create(email=email)

    return render(request, "social.html")


# Delete Training Managment
def del_training(request, id):
    training = Training.objects.get(id=id)
    training.soft_delete()
    messages.error(request, "Successfully ! Training is Deleted  ")
    return redirect("/admin/training/")


@login_required(login_url="/admin/")
def subadmin(request):
    user_subadmin = User.objects.filter(roll="Subadmin", soft_del_status=0).order_by(
        "-created_at"
    )

    Per = Permission.objects.filter(user=request.user)
    page = request.GET.get("page", 1)
    paginator = Paginator(user_subadmin, 10)

    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    userdata = User.objects.all()
    return render(
        request,
        "subadmin/subadmin.html",
        {
            "user_subadmin": user_subadmin,
            "users": users,
            "Per": Per,
            "userdata": userdata,
        },
    )


@login_required(login_url="/admin/")
def add_subadmin(request):
    try:
        if request.method == "POST":
            Name = request.POST.get("Name")
            email = request.POST.get("email")
            mobile_number = request.POST.get("phone")
            address = request.POST.get("address")
            subadmin = request.POST.get("subadmin")
            status = request.POST.get("status")
            permission = request.POST.getlist("name[]")

            code = mobile_number.split(" ")[0]
            phone = mobile_number.split(" ")[1]
            gen_pass = generatePassword()
            sub = User.objects.create(
                username=Name,
                password=make_password(gen_pass),
                user_status=status,
                email=email,
                mobile_number=phone,
                country_code=code,
                address=address,
                roll=subadmin,
            )
            send_to = [email]
            subject = "Your Password is Here "
            content = "Hi" + Name + " Your Zenerated Password is  " + gen_pass
            sendMail(subject, content, send_to)
            for i in permission:
                user = User.objects.get(id=sub.id)
                user.user_permissions.add(i)

            messages.success(
                request,
                "Sub admin added successfully ! Please check your email for Login and password",
            )
            return redirect("/admin/subadmin/")
        else:
            userdata = User.objects.all()
            c = ContentType.objects.filter(app_label="staff_admin")

            model_list = [
                "user",
                "training",
                "category",
                "pages",
                "email_templates",
                "global_setting",
            ]

            t = list()
            for i in c:
                if i.model in model_list:
                    t.append(i.id)
                else:
                    pass

            l1 = list()

            for i in t:

                per = Permission.objects.filter(content_type_id=i)

                x = list()
                c = 1
                for i in per:
                    if c == 1:
                        s_name = i.content_type.model.split("_")

                        if len(s_name) > 1:
                            s = ""
                            for name in s_name:
                                if name == 0:
                                    s = name.title()
                                else:
                                    s = s + " " + name.title()
                            x.append(s)
                        else:
                            x.append(s_name[0].title())

                        c += 1
                    else:
                        pass
                    if "view" in i.name:
                        x.append({"View": i.id})

                    if "add" in i.name:

                        x.append({"Add": i.id})
                    elif "change" in i.name:
                        x.append({"Edit": i.id})

                    elif "delete" in i.name:
                        x.append({"Delete": i.id})

                try:
                    l1.append(x)
                except:
                    pass

            return render(request, "subadmin/add.html", {"l": l1, "userdata": userdata})
    except:
        messages.error(request, " Subadmin is created Failed !")
        return redirect("/admin/subadmin/add")


@login_required(login_url="/admin/")
def edit_subadmin(request, slug):
    try:
        if request.method == "POST":

            Name = request.POST.get("Name")
            email = request.POST.get("email")
            mobile_number = request.POST.get("phone")
            address = request.POST.get("address")
            subadmin = request.POST.get("subadmin")
            status = request.POST.get("status")
            permission = request.POST.getlist("name[]")

            # if User.objects.get(email=email):
            #     messages.error(request, 'Email allready taken')
            #     return redirect('/admin/subadmin/edit/' + slug)

            if mobile_number == None or mobile_number == "":
                sub = User.objects.filter(slug=slug).update(
                    username=Name,
                    user_status=status,
                    email=email,
                    address=address,
                    roll=subadmin,
                )
            else:
                code = mobile_number.split(" ")[0]
                phone = mobile_number.split(" ")[1]
                sub = User.objects.filter(slug=slug).update(
                    username=Name,
                    user_status=status,
                    email=email,
                    mobile_number=phone,
                    country_code=code,
                    address=address,
                    roll=subadmin,
                )
            user = User.objects.get(slug=slug)
            user.user_permissions.clear()

            for i in permission:
                user = User.objects.get(slug=slug)

                user.user_permissions.add(i)
            messages.success(request, " Successfully ! Subadmin is Updated ")
            return redirect("/admin/subadmin/")

        else:
            users = User.objects.filter(slug=slug)
            userdata = User.objects.all()
            try:
                u = User.objects.get(slug=slug)
            except:
                messages.error(request, " Subadmin is created Failed !")
                return redirect("/admin/subadmin/edit/" + slug)

            c = ContentType.objects.filter(app_label="staff_admin")
            model_list = [
                "user",
                "training",
                "global_setting",
                "category",
                "email_templates",
                "pages",
            ]
            t = []
            for i in c:
                if i.model in model_list:
                    t.append(i.id)
                else:
                    pass

            l1 = []

            for i in t:

                per = Permission.objects.filter(content_type_id=i)

                x = []
                c = 1
                for i in per:
                    if c == 1:
                        s_name = i.content_type.model.split("_")

                        if len(s_name) > 1:
                            s = ""
                            for name in s_name:
                                if name == 0:
                                    s = name.title()
                                else:
                                    s = s + " " + name.title()
                            x.append(s)
                        else:
                            x.append(s_name[0].title())

                        c += 1
                    else:
                        pass
                    if "view" in i.name:
                        x.append({"View": i.id})

                    if "add" in i.name:

                        x.append({"Add": i.id})
                    elif "change" in i.name:
                        x.append({"Edit": i.id})

                    elif "delete" in i.name:
                        x.append({"Delete": i.id})

                try:
                    l1.append(x)
                except:
                    pass

            permission_id = u.user_permissions.filter(user__slug=slug)
            l = []
            for i in permission_id:

                l.append(i.id)
            return render(
                request,
                "subadmin/edit.html",
                {"users": users, "userdata": userdata, "l": l1, "list": l},
            )
    except:
        messages.error(request, "Email Allready taken")
        return redirect("/admin/subadmin/edit/" + slug)


# def del_submin(request, id):
#     user = User.objects.get(id=id)
#     user.soft_delete()
#     messages.error(request, "delete subadmin")
#     return redirect('/admin/subadmin')


def del_submin(request, id):

    instance = User.objects.get(id=id)

    instance.soft_delete()
    request.session["subadmin"] = instance.soft_del_status
    del request.session["subadmin"]

    messages.error(request, "Successfully ! Subadmin is deleted")
    return redirect("/admin/subadmin/")


@login_required(login_url="/admin/")
def contact(request):
    try:
        con = ContactUs.objects.all().order_by("-create_at")
    except:
        con = False
    page = request.GET.get("page", 1)
    paginator = Paginator(con, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, "contact.html", {"con": con, "users": users})


@login_required(login_url="/admin/")
def contact_reply(request, id):
    if request.method == "POST":

        email = request.POST.get("email")

        sub = request.POST.get("sub")
        content = request.POST.get("content")
        send_to = [email]

        subject = sub
        content = content
        sendMail(subject, content, send_to)

    reply = ContactUs.objects.get(id=id)

    return render(request, "contact_reply.html", {"reply": reply})


@login_required(login_url="/admin/")
def del_contact(request, id):

    reply = ContactUs.objects.get(id=id)
    reply.soft_delete()
    messages.error(request, "Successfully ! Contact is deleted")
    return redirect("/admin/contact/")


@login_required(login_url="/admin/")
def App_intro(request):
    intro = AppWebIntro.objects.all()
    return render(request, "cms_pages/intro/intro.html", {"intro": intro})


def edit_App_intro(request, slug):
    try:
        if request.method == "POST":
            slug = request.POST.get("slug")

            title = request.POST.get("title")
            Image = request.FILES.get("img")

            Discription = request.POST.get("editor")
            intro = AppWebIntro.objects.get(slug=slug)

            if Image is None:

                intro.slug = slug
                intro.title = title
                intro.textarea = Discription
                intro.save()
                messages.success(request, "Successfully !!! Data Is Updated")

                return redirect("/admin/introduction/")

            else:
                fs = FileSystemStorage()
                filename = fs.save(Image.name, Image)
                intro.slug = slug
                intro.title = title
                intro.image = Image
                intro.textarea = Discription
                intro.save()
                messages.success(request, "Successfully !!! Data Is Updated")

                return redirect("/admin/introduction/")
        intro = AppWebIntro.objects.get(slug=slug)
        return render(request, "cms_pages/intro/edit.html", {"intro": intro})
    except:
        messages.error(request, "Something Went Wrong ")
        return redirect("/admin/introduction/")


def content_management(request, slug):
    try:
        term = ContentManagement.objects.get(slug=slug)

        if request.method == "POST":
            t = request.POST.get("slug")
            title = request.POST.get("editor")
            print(title, "dddddddddddddddddd")
            desc = request.POST.get("editor1")
            print(desc, "dddddddddddddddd")

            save_t = ContentManagement.objects.get(slug=slug)
            save_t.title = title
            save_t.desc = desc
            save_t.save()
            messages.success(request, "Term And Condition is Updated")
            return redirect("/admin/content/management/" + slug)
    except:
        pass

    return render(request, "term-and-condition.html", {"term": term})


# @api_view([ 'GET','POST'])
# @csrf_exempt
# def s_api(request):
#     if request.method == 'GET':
#         s = s_test.objects.all()
#         serializer = s_testSerializer(s, many=True)
#         print(serializer.data, "gggggggggggggggggggggggggggggggggggggggggggggggggggg")

#         return JsonResponse(serializer.data ,safe=False)
#     elif request.method =='POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         number = request.POST.get('number')
#         message = request.POST.get('message')
#         # print(name, email, number, message)
#         serializer = s_testSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data ,"gggggggggggggggggggggggggggggggggggggggg")
#             return JsonResponse({"status": "success", "message": "APi Bana DI hai mene !!!!"}, status=200)
#         return JsonResponse({"status": "error", "message": "Error Api !!!!"}, status=200)


# @api_view(['GET', 'PUT' ,'DELETE'])
# @csrf_exempt
# def s_api_details(request, id):
#     s = s_test.objects.get(id=id)
#     if request.method == 'GET':

#         serializer = s_testSerializer(s)

#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         serializer = s_testSerializer(s, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({"status": "success", "message": "APi Update kr DI hai mene !!!!"}, status=200)
#         return JsonResponse({"status": "error", "message": "Error Api !!!!"}, status=200)

#     elif request.method == 'DELETE':
#         s.delete()
#         return HttpResponse(status=204)
@login_required(login_url="/admin/")
def aboutus(request):
    about = AboutUs.objects.all()
    return render(request, "cms_pages/about/aboutus.html", {"about": about})


def edit_aboutus(request, slug):
    # try:

    if request.method == "POST":
        slug = request.POST.get("slug")
        title = request.POST.get("title")
        discripion = request.POST.get("discripion")
        # img2 = request.FILES.get('img2')
        img2 = request.FILES.get("img2")
        if img2 is None:

            about = AboutUs.objects.get(slug=slug)
            about.title = title
            about.discripion = discripion

            about.save()
            messages.success(request, "Successfully !!! Data Is Updated")

            return redirect("/admin/aboutus/")

        if img2:
            fs = FileSystemStorage()
            filename = fs.save(img2.name, img2)
            about = AboutUs.objects.get(slug=slug)
            about.title = title
            about.discripion = discripion
            about.image = img2
            about.save()
            messages.success(request, "Successfully !!! Data Is Updated")
            return redirect("/admin/aboutus/")
    # except:
    #     messages.error(request, 'Something went wrong')
    #     return redirect('/admin/aboutus/')
    about = AboutUs.objects.get(slug=slug)
    return render(request, "cms_pages/about/edit.html", {"about": about})


@login_required(login_url="/admin/")
def team(request):
    team = meet_our_team.objects.all()

    return render(request, "cms_pages/about/team/team.html", {"team": team})


def add_team(request):
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get("img2")
        discripion = request.POST.get("discripion")
        try:
            if image is None:
                team = meet_our_team.objects.create(name=name, discripion=discripion)
                messages.success(request, "Successfully !!! Updated Data")
        except:
            messages.success(request, "Please Select Correct Image")
        try:
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                team = meet_our_team.objects.create(
                    name=name, image=image, discripion=discripion
                )
                messages.success(request, "Successfully !!! Created Data")
                return redirect("/admin/team/")

        except:
            messages.error(request, "Please Select Correct Image")

            return redirect("/admin/team/add/")

        return redirect("/admin/team/")
    return render(request, "cms_pages/about/team/add.html")


def edit_team(request, slug):
    try:
        if request.method == "POST":
            slug = request.POST.get("slug")
            name = request.POST.get("name")
            image = request.FILES.get("img2")
            discripion = request.POST.get("discripion")
            team = meet_our_team.objects.get(slug=slug)
            try:
                if image is None:

                    team.name = name
                    team.discripion = discripion
                    team.save()
                    messages.success(request, "Successfully !!! Updated Data")
            except:
                messages.success(request, "Please Select Correct Image")

            try:
                if image:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)
                    team.name = name
                    team.image = image
                    team.dicripion = discripion
                    team.save()
                    messages.success(request, "Successfully !!! Updated Data")

                    return redirect("/admin/team/")
            except:
                messages.error(request, "Please Select Correct Image")

                return redirect("/admin/team/edit/" + slug)

        team = meet_our_team.objects.get(slug=slug)
        return render(request, "cms_pages/about/team/edit.html", {"team": team})
    except:
        messages.error(request, "SomeThing Went Wrong")
        return redirect("/admin/team/edit/" + slug, {"team": team})


@login_required(login_url="/admin/")
def del_team(request, id):

    team = meet_our_team.objects.get(id=id)
    team.delete()
    messages.error(request, "Successfully ! Data Is Deleted")
    return redirect("/admin/team/")


def post_create(request):
    try:
        usr = request.user
    except:
        usr: None
    no_list = [i for i in range(1, 99)]
    try:
        obj = Category.objects.all()
    except:
        obj = None
    if request.method == "POST":
        data = request.POST
        el = list(data.items())
        x = el[-1][0]
        a, b = x.split("[")
        val = b[:1]
        t = int(val)
        for i in range(t + 1):
            dates = data[f"shift[{i}]date"]
            time_in = data[f"shift[{i}]time_in"]
            time_out = data[f"shift[{i}]time_out"]
            employer = data[f"shift[{i}]employer"]
            positions = data[f"shift[{i}]position"]
            desc = data[f"shift[{i}]desc"]
            salary = data[f"shift[{i}]salary"]
            showtime = strftime("%Y-%m-%d", gmtime())

            time_in_in = showtime + " " + time_in

            time_out_out = showtime + " " + time_out
            # print(type(time_in),type(time_out))
            # print(time_in,time_out)
            # date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
            # x_in=datetime.combine(d,time_in)
            # y_out=datetime.combine(d,time_out)
            # print(x_in)
            # print(type(x_in))
            # try:
            sr = Shift_Post.objects.latest("id").id + 1000
            Shift_Post.objects.create(
                date=dates,
                in_time=time_in_in,
                out_time=time_out_out,
                employee_id=employer,
                position_id=positions,
                text_field=desc,
                wages=salary,
                serial_no=sr + 1,
            )
            print(sr, "dddddddddddddddddddd")
            # except:
            #     sr=1000
            #     messages.success(request,'Successfully ! Noooooooooooo Shift Post Created')

        messages.success(request, "Successfully ! New Shift Post Created")

        return redirect("/admin/manage/shift/")

    employer = User.objects.filter(roll="employer")
    print("ddddddddddddddddddddddddddddddddddddd")
    return render(
        request,
        "shifts/post-create.html",
        {"employer": employer, "number": no_list, "category": obj},
    )


def manage_shift(request):
    new_post = (
        Shift_Post.objects.exclude(pending=True)
        .exclude(completed=True)
        .exclude(accepted=True)
    )
    accpeted_shift = (
        Shift_Post.objects.filter(accepted=True)
        .exclude(completed=True)
        .exclude(pending=True)
    )
    pending_shift = Shift_Post.objects.filter(pending=True)
    completed_shift = Shift_Post.objects.filter(completed=1)
    return render(
        request,
        "shifts/manage-shift.html",
        {
            "accepted_shift": accpeted_shift,
            "new_post": new_post,
            "pending_shift": pending_shift,
            "completed_shift": completed_shift,
        },
    )


def query(request):
    q = Query.objects.all()
    return render(request, "query.html", {"q": q})


def view_query(request, id):
    q = Query.objects.get(id=id)

    # print(r, "dddddddddddddddddddddd")
    data = QueryMessage.objects.filter(query_id=id)
    for i in data:
        print(i, "dddddddddddddddddddd")
    print(data, "ssssssssssssssssss")
    for i in data:
        query_id = i.query_id
        # name = i.name
        receiver_id = i.sender_id
        # sname = i.sender.fname
        # rname = i.reciver.fname
        # print(, "dddddddddddddddddddddddd")
        sender_id = request.user.id
        # print( "ffffffffffffffffffffffffffffffffffffffff")
    if request.method == "POST":
        reply = request.POST.get("reply")
        # print(reply, "ddddddddddddddddddddddddddddddd")
        query_save = QueryMessage.objects.create(
            query_id=query_id,
            sender_id=sender_id,
            reciver_id=receiver_id,
            message=reply,
        )
        return redirect("/admin/view/query/" + str(id))
    return render(request, "query_reply.html", {"data": data})


def delete_query(request, id):
    query = Query.objects.get(id=id)
    query.delete()
    return redirect("/admin/query")
