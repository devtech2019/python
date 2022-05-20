from ast import Try
from atexit import register
from contextlib import redirect_stderr
from email import message
from email.mime import image
from urllib.request import Request
from django.shortcuts import render, redirect
import staff_admin
from .helpers import *
from django.utils.html import strip_tags
from .models import *
from staff_admin.models import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as login_check
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import pgeocode
from geopy.geocoders import Nominatim
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.core.mail import send_mail
from staff_admin.helpers import generateOTP
from applicant_web.models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from dateutil import parser
from allauth.socialaccount.models import SocialAccount
import geopandas

User = get_user_model()

# Create your views here.


def home(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass
    except:
        pass

    try:
        section1 = pages.objects.get(id=1)
    except:
        section1 = None
    try:
        section2 = pages.objects.get(id=2)
    except:
        section2 = None
    try:
        section3 = pages.objects.get(id=3)
    except:
        section3 = None
    try:
        section4 = pages.objects.get(id=4)
    except:
        section4 = None
    try:
        section5 = pages.objects.get(id=5)
    except:
        section5 = None
    try:
        section6 = pages.objects.get(id=6)
    except:
        section6 = None
    try:
        section7 = pages.objects.get(id=7)
    except:
        section7 = None
    try:
        section8 = pages.objects.get(id=8)
    except:
        section8 = None

    # section4 = pages.objects.get(id=4)
    # section5 = pages.objects.get(id=5)
    # section6 = pages.objects.get(id=6)
    # section7 = pages.objects.get(id=7)

    # p = pages.objects.get(id=1)
    # p2 = pages.objects.get(id=2)

    # section4 = pages.objects.get(id=6)
    # section5 = pages.objects.get(id=7)
    qr_code = Qr_Code.objects.all()
    return render(
        request,
        "dashboard/index.html",
        {
            "qr_code": qr_code,
            "section1": section1,
            "section2": section2,
            "section3": section3,
            "section4": section4,
            "section5": section5,
            "section6": section6,
            "section7": section7,
            "section8": section8,
        },
    )


def Contact(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        subject = request.POST.get("sub")
        print(subject, "ffffffffffffffffffffffffffffffff")
        message = request.POST.get("message")

        contact = ContactUs.objects.create(
            First_name=first_name,
            sub=subject,
            Last_name=last_name,
            email=email,
            message=message,
        )
        contact.save()
        return JsonResponse(
            {"status": "success", "message": "Details Submitted Successfully !!!!"},
            status=200,
        )
    else:
        return JsonResponse(
            {"status": "error", "message": "No Details Saved !!!!"}, status=200
        )


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")
        u = User.objects.filter(roll="employer")

        try:
            v = User.objects.get(email=email)
            request.session["email"] = email
            user = auth.authenticate(email=email, password=password)
        except:
            messages.error(request, "invalid username or password ")
            return redirect("/login/")

        if user is None:
            messages.error(request, "invalid username or password ")
            return redirect("/login/")
        # if user:
        #     messages.error(request, "invalid username or password ")
        #     return redirect("/login/")

        if user.roll == "applicant":
            messages.error(request, "invalid username or password ")
            return redirect("/login/")

        if user.roll == "employer":
            try:
                em = email_templates.objects.get(id=3)
                otp = generateOTP()
                v.OTP = otp
                v.save()
                send_to = [email]
                subject = em.sub

                content = em.content

                t = strip_tags(content)
                c = t.replace("{name}", v.first_name + "" + v.last_name)
                msg = c.replace("{OTP}", otp)
                sendMail(subject, msg, send_to)
                messages.success(request, "OTP Sent Successfully !!!")
                return redirect("/login/otp/" + v.slug)
            except:
                em = None
                messages.error(request, "Something Went Wrong")
                return redirect("/login/otp/" + v.slug)

        if user.roll == "employer " is None:
            messages.error(request, "invalid username or password ")
            return redirect("/login/")
    return render(request, "employer/auth/login.html")


def login_otp(request, slug):
    try:
        user = User.objects.get(slug=slug)
        if request.method == "POST":
            otp1 = request.POST.get("otp1")
            otp2 = request.POST.get("otp2")
            otp3 = request.POST.get("otp3")
            otp4 = request.POST.get("otp4")
            Otp = str(otp1) + str(otp2) + str(otp3) + str(otp4)

            if Otp == user.OTP:
                if user.user_status == True:
                    # auth.logout(request)
                    messages.error(request, "Permission denied")

                    return redirect("/login/")
                if user.company_profile_status == True:

                    auth.login(request, user)
                    return redirect("/")

                elif user.company_profile_status == False:

                    return redirect("/profile/company-profile/" + user.slug)
                else:
                    messages.success(request, user.first_name, "Login Successfully")
                    auth.login(request, user)
                    return redirect("/")
            else:
                messages.error(request, "Otp does not match")
                return redirect("/login/otp/" + slug)
        return render(request, "employer/auth/login-otp.html", {"user": user})
    except:
        messages.error(request, "Otp does not match")
        return redirect("/login/otp/" + slug)


def resend_otp(request, slug):
    try:
        m = User.objects.get(OTP_string=slug)
        em = email_templates.objects.get(id=3)
        print(em, "dddddddddddddddddddddddddddddddddd")
        o = generateOTP()
        m.OTP = o
        m.save()
        send_to = [m.email]
        subject = em.sub
        print(subject, "subjectsssssssssssssssssssssssss")
        content = em.content
        print(content, "subjectsssssssssssssssssssssssss")
        otp = o
        name = m.first_name + " " + m.last_name
        t = strip_tags(content)
        c = t.replace("{name}", name)
        msg = c.replace("{OTP}", otp)
        sendMail(subject, msg, send_to)
        messages.success(request, "Otp sent successfully")

        return redirect("/verifyotp/" + slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect("/verifyotp/" + slug)


def logout(request):
    auth.logout(request)
    return redirect("/login/")


def about_us(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    team = meet_our_team.objects.all()
    about_section_1 = AboutUs.objects.get(id=1)
    about_section_2 = AboutUs.objects.get(id=2)
    # about_section_3 = AboutUs.objects.get(id=3)

    print(about_section_1.image, "fffffffffffffffff")
    return render(
        request,
        "employer/emp_pages/about-us.html",
        {
            "about_section_1": about_section_1,
            "about_section_2": about_section_2,
            "team": team,
        },
    )


def emp_country_ajax(request):
    country = request.POST.get("select_country")
    state = States.objects.filter(country_id=country).values()
    print(state, "ffffffffffffffffffffffff")
    if state is None:
        return JsonResponse(
            {"status": "error", "message": " no changed !!!!"}, status=200
        )
    else:

        return JsonResponse(
            {"status": "success", "message": "changed !!!!", "result": list(state)},
            status=200,
        )


def emp_state_city_ajax(request):
    state = request.POST.get("state_value")
    city = Cities.objects.filter(state_id=state).values()
    if city is None:
        return JsonResponse(
            {"status": "error", "message": " no changed !!!!"}, status=200
        )
    else:

        return JsonResponse(
            {"status": "success", "message": "changed !!!!", "result": list(city)},
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


# def qr_code(request):
#
#     print(qr_code,"gggggggggggggggggggggggggggggggggggggggg")
#     return render(request, 'index.html',{'qr_code':qr_code})


def forgotpassword(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            request.session["email"] = email
            # print(email,"ffffffffffffffffffffffffffffff")
            m = User.objects.get(email=email)
            # print(m.first_name)
            # print(e,"ddddddddddddd")
            em = email_templates.objects.get(id=3)
            if m.roll == "applicant":
                messages.error(
                    request, "Staff Does Not Have Permission for forgot password"
                )
                print("noooooooo found")
                return redirect("/forgotpassword/")

            if m.roll == "employer":
                o = generateOTP()
                us = hash(o)
                m.OTP_string = us
                m.OTP = o
                m.save()

                send_to = [email]

                subject = em.sub
                content = em.content

                otp = o
                name = m.first_name + " " + m.last_name
                t = strip_tags(content)
                c = t.replace("{name}", name)
                msg = c.replace("{OTP}", otp)
                print(msg)
                sendMail(subject, msg, send_to)

                return redirect("/verifyotp/" + str(us))
            else:
                messages.error(request, "Email Does Not Exits")
                print("noooooooo found")
                return redirect("/forgotpassword/")

    except:
        messages.error(request, "Email is not exist")
        return redirect("/forgotpassword/")

    return render(request, "employer/auth/forgot-password.html")


def verify_otp(request, slug):
    m = User.objects.get(OTP_string=slug)
    if request.method == "POST":
        otp1 = request.POST.get("otp1")
        otp2 = request.POST.get("otp2")
        otp3 = request.POST.get("otp3")
        otp4 = request.POST.get("otp4")
        Otp = str(otp1) + str(otp2) + str(otp3) + str(otp4)

        if m.OTP == Otp:

            return redirect("/passwordresetform/" + slug)
        else:
            print("not match")
            messages.error(request, "Otp does not match")
            return redirect("/verifyotp/" + slug)

    return render(request, "employer/auth/forgot-otp.html", {"m": m})


def passwordresetform(request, slug):

    if request.method == "POST":
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("confirm-new-password")
        if new_password is None:
            messages.error(request, "Please Fill Password ")
            return redirect("passwordresetform")
        elif new_password == confirm_password:
            m = User.objects.filter(OTP_string=slug).update(
                password=make_password(new_password)
            )

            messages.success(request, "Password Changed Successfully")
            return redirect("/login/")
        else:

            return redirect("passwordresetform")
    return render(request, "employer/auth/reset-password-form.html")


def user_profile(request, slug):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    if request.method == "POST":
        slug = request.POST.get("slug")
        company = request.POST.get("Cname")
        first_name = request.POST.get("Fname")
        last_name = request.POST.get("Lname")
        mobile_number = request.POST.get("mob_num")
        address = request.POST.get("address")

        users = User.objects.get(slug=request.user.slug)
        users.slug = slug
        users.company = company
        users.first_name = first_name
        users.last_name = last_name
        users.mobile_number = mobile_number
        users.address = address
        users.save()

        messages.success(request, "Profile Update successfully")
        return redirect("/profile/" + slug)
    else:

        user = User.objects.get(slug=request.user.slug)
        # print(user,"ddddddddddddddd")
        try:
            users = CompanyInfo.objects.get(user_id=user.id)
            users.user_slug = user.slug
            users.save()

        except:
            users = None
            messages.error(request, "Admin Do not Have Company InFo")
            return redirect("/")
        # messages.success(request, 'Nooooooooooooooooooooo')
    return render(request, "userprofile/profile.html", {"user": user, "slug": slug})

    # print(users.user_slug, "ffffffffffffffffffffffffff")
    # except:
    #     messages.error(request, 'Some Went Wrong')
    #     return redirect('/profile/')


def update_company_profile(request, user_slug):

    if request.method == "POST":
        user = request.POST.get("user_slug")
        print(user, "ffffffffffffffffff")
        company = request.POST.get("Cname")
        phone_number = request.POST.get("mob_num")
        fax = request.POST.get("fax")
        address = request.POST.get("address")
        year_in_bussiness = request.POST.get("year_in_bussiness")
        solo = request.POST.get("sole_proprietorship")
        partnership = request.POST.get("partnership")
        corporation = request.POST.get("corporation")
        other = request.POST.get("other")
        tax = request.POST.get("tax")

        com = CompanyInfo.objects.get(user_id=request.user.id)
        com.name = company
        com.fax = fax
        com.address = address
        com.corporation = corporation

        com.phone_number = phone_number
        com.year_of_business = year_in_bussiness
        com.solo = solo
        com.partnership = partnership
        com.other = other
        com.tax = tax
        com.save()
        messages.success(request, "Company Profile Update successfully")
        return redirect("/client/company-profile/" + user_slug)

    company = CompanyInfo.objects.get(user_slug=user_slug)
    return render(
        request, "userprofile/update_user_company_profile.html", {"company": company}
    )


# def manage_shift(request):
#     return render(request , 'manage-shifts.html')


# def time_sheet(request):
#     return render(request, 'time-sheet.html')


def notifications(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    return render(request, "notification/notifications.html")


def notifications_setting(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    return render(request, "notification/notification-settings.html")


def no_notifications(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    return render(request, "notification/no-notifications.html")


def app_sign_up(request):
    cat = Category.objects.filter(status=1, soft_del_status=0)
    country = Country.objects.all()
    year = list(range(0, 15))
    month = list(range(0, 13))
    year_lists = []
    month_lists = []

    for i in year:
        print(i, "ddddddddddddddddddd")
        year_lists.append(i)
    for i in month:
        month_lists.append(i)

    return render(
        request,
        "applicant/sign-up-applicants.html",
        {"cat": cat, "country": country, "l": year_lists, "m": month_lists},
    )


def app_data_ajax(request):
    if request.method == "POST":
        print("dodikfhjidf")
        id = request.POST.get("id")
        first_name = request.POST.get("FName")
        last_name = request.POST.get("LName")
        mobile_number = request.POST.get("mob_num")
        # latitude = request.POST.get('latitude')
        # print(latitude,"ddddddddddddddd")
        # longitude = request.POST.get('longitude')
        landline = request.POST.get("land_line")
        email = request.POST.get("email")
        position = request.POST.get("position")
        experience = request.POST.get("experience")
        password = request.POST.get("password")
        re_password = request.POST.get("rePassword")
        country = request.POST.get("country")
        # state = request.POST.get("state")
        city = request.POST.get("city")
        postal = request.POST.get("postal_code")
        address = request.POST.get("address")
        year = request.POST.get("year")
        month = request.POST.get("month")
        address2 = request.POST.get("address2")
        code = mobile_number.split(" ")[0]
        phone = mobile_number.split(" ")[1]
        user_type = request.POST.get("user_type")
        df = geopandas.tools.geocode(postal)

        try:
            df["lon"] = df["geometry"].x
            df["lat"] = df["geometry"].y
            lat = df["lat"]
            print(lat, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
            long = df["lon"]
            print(long, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

        except:
            return JsonResponse(
                {"status": "error", "message": " Please select valid pin code !!!!"},
                status=404,
            )

        otp = generateOTP()
        em = email_templates.objects.get(id=3)

        if "@" and "." not in email:
            return JsonResponse(
                {"status": "error", "message": "Invalid Email address !!!!"},
                status=404,
            )

        if User.objects.filter(mobile_number=phone):
            print("fffffffffffffffffffffffff")
            return JsonResponse(
                {"status": "error", "message": "Mobile Number allready exits !!!!"},
                status=404,
            )

        if user_type == "applicant":
            if User.objects.filter(email=email):
                return JsonResponse(
                    {"status": "error", "message": "Email allready exits !!!!"},
                    status=404,
                )

            # if latitude == ' ' or longitude == ' ':
            #     return JsonResponse({"status": "error", "message": " Please select valid address !!!!"}, status=404)

            if password == re_password:
                userdata = User.objects.create(
                    fname=first_name,
                    OTP=otp,
                    latitude=lat,
                    exp_year=year,
                    exp_month=month,
                    address=address,
                    address2=address2,
                    longitude=long,
                    lname=last_name,
                    country=country,
                    # state=state,
                    city=city,
                    post_code=postal,
                    email=email,
                    password=make_password(password),
                    mobile_number=phone,
                    landline=landline,
                    country_code=code,
                    position_id=position,
                    experience=experience,
                    roll=user_type,
                )
                unique_id = userdata.id + 100
                send_to = [email]
                subject = em.sub
                content = em.content
                t = strip_tags(content)
                c = t.replace("{name}", first_name + "" + last_name)
                msg = c.replace("{OTP}", otp)
                sendMail(subject, msg, send_to)
                slug = userdata.slug

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Applicant Sign Up Completed !!!!",
                        "slug": slug,
                    },
                    status=200,
                )

            else:
                return JsonResponse(
                    {"status": "error", "message": "Password Does not match!!!!"},
                    status=404,
                )
    return JsonResponse({"status": "error", "message": " No changed !!!!"}, status=404)


def app_resend_otp(request, slug):
    try:
        m = User.objects.get(slug=slug)
        em = email_templates.objects.get(id=3)

        o = generateOTP()
        m.OTP = o
        m.save()
        send_to = [m.email]
        subject = em.sub
        content = em.content
        otp = o
        name = m.first_name + " " + m.last_name
        t = strip_tags(content)
        c = t.replace("{name}", name)
        msg = c.replace("{OTP}", otp)
        sendMail(subject, msg, send_to)
        messages.success(request, "Otp sent successfully")
        return redirect("/applicant/otp-verify/" + slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect("/applicant/otp-verify/" + slug)


def app_vaccation_information(request, slug):

    user = User.objects.get(slug=slug)
    print(user.slug)
    if request.method == "POST":
        vaccination = request.POST.get("Vaccination")
        booster = request.POST.get("booster")
        image = request.FILES.get("image")
        # city = request.POST.get('city')
        dob = request.POST.get("date_of_birth")
        # position = request.POST.get("position")
        Mnc_pin = request.POST.get("nmc_pin")

        recitation = request.POST.get("flexCheckyes")
        if recitation == "True":
            print("ssssssssssssssssssssssssss")
            dbc = request.POST.get("DBC")
            print(dbc, "ggggggggggggggggggggggggggggggggg")

            recitations_desc = request.POST.get("recitations_desc")
            print(recitations_desc, "ggggggggggggggggggggggggggggggggg")

            DBC_Issues_Date = request.POST.get("DBC_Issues_Date")
            DBC_status = request.POST.get("DBC_status")
            work_checkes = request.POST.get("flexCheckyesrt")
            print(work_checkes, "tttttttttttttttttttttttttt")
            work_preference = request.POST.get("flexCheckyespre")
            print(work_preference, "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
            emergency = request.POST.get("emergency")
            training = request.POST.get("training")
            training_start_date = request.POST.get("training_start")
            training_end_date = request.POST.get("training_end")
            # 🖘 raise error if greater than
            if datetime.strptime(DBC_Issues_Date, "%Y-%m-%d") > datetime.now():
                messages.error(request, "Please Select Correct DBC issue Date ")
                return redirect("/applicant/vaccination/" + slug)

            elif datetime.strptime(training_start_date, "%Y-%m-%d") > datetime.now():
                messages.error(request, "Please Select Correct Training Start Date ")
                return redirect("/applicant/vaccination/" + slug)

            elif datetime.strptime(training_end_date, "%Y-%m-%d") > datetime.now():
                messages.error(request, "Please Select Training end Date ")
                return redirect("/applicant/vaccination/" + slug)
            try:
                # if ApplicantDeatails.objects.get(user_id=user.id):
                #     data = ApplicantDeatails.objects.filter(user_id=user.id).update(
                #         vaccinated=vaccination,
                #         booster_dose=booster,
                #         dob=dob,
                #         work_checkes=work_checkes,
                #         work_preference=work_preference,
                #         nmc_pin=NMC_pin,
                #         recitation=recitation,
                #         enhance_dbc=dbc,
                #         recitation_desc=recitations_desc,
                #         enhance_dbc_issue=DBC_Issues_Date,
                #         dbc_status=DBC_status,
                #         emergency_no=emergency,
                #         training_id=training,
                #         training_start_date=training_start_date,
                #         training_end_date=training_end_date,
                #     )
                #     messages.error(request, "Please Select Training end Date ")
                #     return redirect("/applicant/vaccination/" + slug)

                if image is None:
                    data = ApplicantDeatails.objects.create(
                        user_id=user.id,
                        vaccinated=vaccination,
                        booster_dose=booster,
                        dob=dob,
                        work_checkes=work_checkes,
                        work_preference=work_preference,
                        Mnc_pin=Mnc_pin,
                        recitation=recitation,
                        enhance_dbc=dbc,
                        recitation_desc=recitations_desc,
                        enhance_dbc_issue=DBC_Issues_Date,
                        dbc_status=DBC_status,
                        emergency_no=emergency,
                        training_id=training,
                        training_start_date=training_start_date,
                        training_end_date=training_end_date,
                    )
                    messages.success(request, "Form Submitted Successfully")
                    auth.logout(request)
                    return redirect("/")
                else:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)

                    data = ApplicantDeatails.objects.create(
                        user_id=user.id,
                        vaccinated=vaccination,
                        booster_dose=booster,
                        image=image,
                        dob=dob,
                        work_checkes=work_checkes,
                        work_preference=work_preference,
                        Mnc_pin=Mnc_pin,
                        recitation=recitation,
                        enhance_dbc=dbc,
                        recitation_desc=recitations_desc,
                        enhance_dbc_issue=DBC_Issues_Date,
                        dbc_status=DBC_status,
                        emergency_no=emergency,
                        training_id=training,
                        training_start_date=training_start_date,
                        training_end_date=training_end_date,
                    )
                    messages.success(request, "Form Submitted Successfully")
                    auth.logout(request)
                    return redirect("/")
            except:
                messages.error(request, "Something went wrong")
                return redirect("/applicant/vaccination/" + slug)
        else:
            # if datetime.strptime(dob, "%Y-%m-%d") > datetime.now():
            #     messages.error(request, "Please Select Correct Date of Birth  Date ")
            #     return redirect("/applicant/vaccination/" + slug)

            print("dsdhvbgshdsdsafadsgadg")
            # if ApplicantDeatails.objects.get(user_id=user.id):
            #     data = ApplicantDeatails.objects.filter(user_id=user.id).update(
            #         vaccinated=vaccination,
            #         booster_dose=booster,
            #         dob=dob,
            #         nmc_pin=NMC_pin,
            #         recitation=recitation,
            #     )
            #     print("wwwwwwwwwwwwwwwwwwwwwwwww")

            #     messages.error(request, "Please Select Training end Date ")
            #     return redirect("/applicant/vaccination/" + slug)
            try:
                if image is None:
                    data = ApplicantDeatails.objects.create(
                        user_id=user.id,
                        vaccinated=vaccination,
                        booster_dose=booster,
                        dob=dob,
                        Mnc_pin=Mnc_pin,
                        recitation=recitation,
                    )
                    messages.success(request, "Form Submitted Successfully")
                    auth.logout(request)
                    print("tttttttttttttttttttttttttttttttttttt")

                    return redirect("/")
                else:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)

                    data = ApplicantDeatails.objects.create(
                        user_id=user.id,
                        vaccinated=vaccination,
                        booster_dose=booster,
                        image=image,
                        dob=dob,
                        Mnc_pin=Mnc_pin,
                        recitation=recitation,
                    )
                    print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyy")

                    messages.success(request, "Form Submitted Successfully")
                    auth.logout(request)

                    return redirect("/")
            except:
                messages.error(request, "Something went wrong")
                return redirect("/applicant/vaccination/" + slug)

    else:
        training = Training.objects.all()
        cat = Category.objects.all()
        date = datetime.now()
        m = date.date()
        print(m, "fffffffffffffffffffffffffffff")

        return render(
            request,
            "applicant/sign-up-after-submit-applicants.html",
            {
                "cat": cat,
                "training": training,
                "user_name": user.fname + " " + user.lname,
                "date": m,
            },
        )

    # training = Training.objects.all()
    # cat = Category.objects.all()
    # return render(
    #     request,
    #     "applicant/sign-up-after-submit-applicants.html",
    #     {
    #         "cat": cat,
    #         "training": training,
    #         "user_name": user.fname + " " + user.lname,
    #     },
    # )


def emp_sign_up(request):
    userdata = User.objects.all()
    country = Country.objects.all()

    return render(
        request,
        "client/sign-up-employers.html",
        {"userdata": userdata, "country": country},
    )


def emp_data_ajax(request):

    if request.method == "POST":
        company_profile_status = request.POST.get("company_profile_status")
        first_name = request.POST.get("FName")
        last_name = request.POST.get("LName")
        # latitude = request.POST.get('latitude')
        # longitude = request.POST.get('longitude')
        company_name = request.POST.get("CName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("rePassword")
        mobile_number = request.POST.get("mob_num")
        address = request.POST.get("address")
        code = mobile_number.split(" ")[0]
        phone = mobile_number.split(" ")[1]
        country = request.POST.get("country")
        # state = request.POST.get("state")
        city = request.POST.get("city")
        postal = request.POST.get("postal_code")
        user_type = request.POST.get("user_type")
        df = geopandas.tools.geocode(postal)

        try:
            df["lon"] = df["geometry"].x
            df["lat"] = df["geometry"].y
            lat = df["lat"]
            print(lat, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
            long = df["lon"]
            print(long, "gggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

        except:
            return JsonResponse(
                {"status": "error", "message": " Please select valid pin code !!!!"},
                status=404,
            )

        # print(df['lon'], 'lattttttttttttttttttttttttttt')
        # print(df['lat'], 'longggggggggggggggggggggggggggggggggggg')

        otp = generateOTP()
        em = email_templates.objects.get(id=3)

        if "@" and "." not in email:
            return JsonResponse(
                {"status": "error", "message": "Invalid Email address !!!!"},
                status=404,
            )

        if User.objects.filter(mobile_number=phone):
            print("fffffffffffffffffffffffff")
            return JsonResponse(
                {"status": "error", "message": "Mobile Number allready exits !!!!"},
                status=404,
            )

        if user_type == "employer":
            print("sdfsfsfsfs")

            if User.objects.filter(email=email):
                return JsonResponse(
                    {"status": "error", "message": "email allready exits !!!!"},
                    status=404,
                )

            # if lat == ' ' or long == ' ':
            #     return JsonResponse({"status": "error", "message": " Please select valid pin code !!!!"}, status=404)

            # if not (lat or long):
            #     return JsonResponse({"status": "error", "message": " Please select valid pin code !!!!"}, status=404)

            if password == re_password:
                userdata = User.objects.create(
                    company_profile_status=company_profile_status,
                    latitude=lat,
                    longitude=long,
                    country=country,
                    # state=state,
                    city=city,
                    post_code=postal,
                    fname=first_name,
                    lname=last_name,
                    company=company_name,
                    email=email,
                    password=make_password(password),
                    mobile_number=phone,
                    OTP=otp,
                    country_code=code,
                    address=address,
                    roll=user_type,
                )
                unique_id = userdata.id + 100
                send_to = [email]
                subject = em.sub
                content = em.content
                t = strip_tags(content)
                c = t.replace("{name}", first_name + "" + last_name)
                msg = c.replace("{OTP}", otp)
                sendMail(subject, msg, send_to)
                # messages.success(
                #     request, " Employer User Created and password sent on mail ")
                slug = userdata.slug

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Sign Up Completed !!!!",
                        "slug": slug,
                    },
                    status=200,
                )

            else:
                return JsonResponse(
                    {"status": "error", "message": "Password Does not match!!!!"},
                    status=404,
                )
        print("sdsdsdssssssss")
    return JsonResponse({"status": "error", "message": " No changed !!!!"}, status=404)


def emp_otp_verify(request, slug):
    return render(request, "client/emp-verification-otp.html", {"slug": slug})


def emp_resend_otp(request, slug):
    m = User.objects.get(slug=slug)
    em = email_templates.objects.get(id=3)

    o = generateOTP()

    m.OTP = o
    m.save()
    send_to = [m.email]

    subject = em.sub

    content = em.content

    otp = o
    print(otp, "otpppppppppppppppppppppppppppppppp")
    name = m.fname + " " + m.lname
    print(name, "ddddddddddddddddddddddddddddddd")
    t = strip_tags(content)
    print(t, "ttttttttttttttttttttttttttt")
    c = t.replace("{name}", name)
    print(c, "hhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    msg = c.replace("{OTP}", otp)
    print(msg, "ggggggggggggggggggggggggggg")
    sendMail(subject, msg, send_to)

    return redirect("/client/otp-verify/" + slug)

    # return redirect( '/client/otp-verify/' + slug)


def app_otp_verify(request, slug):
    return render(request, "applicant/app-verification-otp.html", {"slug": slug})


def otp_verify_ajax(request, slug):
    u = User.objects.get(slug=slug)
    if request.method == "POST":
        otp1 = request.POST.get("otp1")
        otp2 = request.POST.get("otp2")
        otp3 = request.POST.get("otp3")
        otp4 = request.POST.get("otp4")
        Otp = str(otp1) + str(otp2) + str(otp3) + str(otp4)

        if u.OTP == Otp:
            return JsonResponse(
                {"status": "success", "message": "Otp Verified !!!!", "slug": slug}
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Otp Dose not match !!!!", "slug": slug},
            status=404,
        )
    return JsonResponse(
        {"status": "error", "message": "Otp Dose not match!!!!"}, status=404
    )


def emp_company_information(request, slug):
    user = User.objects.get(slug=slug)

    if request.method == "POST":
        name = request.POST.get("Cname")
        phone_number = request.POST.get("mob_num")
        fax = request.POST.get("fax")
        email = request.POST.get("email")
        address = request.POST.get("address")
        year_in_bussiness = request.POST.get("year_in_bussiness")
        sole_proprietorship = request.POST.get("Sole")
        print(sole_proprietorship, "sssssssssssssssssssssssssssss")
        partnership = request.POST.get("partnership")
        print(partnership, "sssssssssssssssssssssssssssss")
        corporation = request.POST.get("corporation")

        redio = request.POST.get("propertytype")

        other = request.POST.get("other")
        tax = request.POST.get("tax")
        try:
            if redio == "1":
                users = CompanyInfo.objects.create(
                    user_id=user.id,
                    name=name,
                    phone_number=phone_number,
                    fax=fax,
                    email=email,
                    address=address,
                    year_of_business=year_in_bussiness,
                    about_company=sole_proprietorship,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                users.save()

                user.company_profile_status = True
                user.save()
                messages.success(request, "Company details saved succssfully !!!! ")
                return redirect("/login/")
            elif redio == "2":
                users = CompanyInfo.objects.create(
                    user_id=user.id,
                    name=name,
                    phone_number=phone_number,
                    fax=fax,
                    email=email,
                    address=address,
                    year_of_business=year_in_bussiness,
                    about_company=partnership,
                    # about_company=corporation,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                users.save()

                user.company_profile_status = True
                user.save()
                messages.success(request, "Company details saved succssfully !!!! ")
                return redirect("/login/")
            elif redio == "3":

                users = CompanyInfo.objects.create(
                    user_id=user.id,
                    name=name,
                    phone_number=phone_number,
                    fax=fax,
                    email=email,
                    address=address,
                    year_of_business=year_in_bussiness,
                    # about_company=partnership,
                    about_company=corporation,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
                users.save()

                user.company_profile_status = True
                user.save()
                messages.success(request, "Company details saved succssfully !!!! ")
                return redirect("/login/")
            else:
                users = CompanyInfo.objects.create(
                    user_id=user.id,
                    name=name,
                    phone_number=phone_number,
                    fax=fax,
                    email=email,
                    address=address,
                    year_of_business=year_in_bussiness,
                    # about_company=partnership,
                    # about_company=corporation,
                    partnership=redio,
                    other=other,
                    tax=tax,
                )
            users.save()

            user.company_profile_status = True
            user.save()
            messages.success(request, "Company details saved succssfully !!!! ")
            return redirect("/login/")
        except:
            messages.error(request, "Something Went Wrong")
            return redirect("/profile/company-profile/" + slug)
        #
    country = Country.objects.all()
    return render(
        request, "client/enter-your-company-information.html", {"country": country}
    )


def Change_password(request):
    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()
        print(u.company_profile_status, "fffffffffffffffffffffffffffffffffffff")
        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass

    except:
        pass
    if request.method == "POST":
        password = request.POST.get("pass")

        new_passowrd = request.POST.get("newpass")
        rnew_passowrd = request.POST.get("cnewpass")
        user = User.objects.get(id=request.user.id)
        print()
        un = user.id

        print(user, "ddddddddddddddd")
        check = user.check_password(password)
        if check == True:
            user.set_password(new_passowrd)
            user.save()
            user = User.objects.get(id=un)
            login_check(request, user)
            messages.success(request, " Password changed Successfully !!!! ")
            return redirect("/client/change-password")
        print(check, "ffffffffffffff")

    return render(request, "change-password.html")
