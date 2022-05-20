from ast import And
from datetime import date
from urllib import request
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import *
from staff_admin.models import *
from employee_web.models import *
from staff_app.helpers import save_data_inObject
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from applicant_web.models import *
from staff_admin.helpers import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from time import gmtime, strftime

# from social_django
# from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialAccount


@login_required(login_url="/login/")
def shiftPostCreate(request):
    # try:
    usr = request.user

    no_list = [i for i in range(1, 99)]

    obj = Category.objects.all()

    if request.method == "POST":
        data = request.POST
        el = list(data.items())
        x = el[-1][0]
        a, b = x.split("[")
        val = b[:1]
        t = int(val)
        print(t)
        for i in range(t + 1):
            dates = data[f"shift[{i}]date"]

            time_in = data[f"shift[{i}]time_in"]
            time_out = data[f"shift[{i}]time_out"]

            positions = data[f"shift[{i}]position"]
            desc = data[f"shift[{i}]desc"]
            salary = data[f"shift[{i}]salary"]
            # showtime = strftime("%Y-%m-%d", gmtime())
            print(dates, "ddddddddddddddddddddd")
            # if dates == showtime:
            #     time_in_in = showtime + " " + time_in

            #     time_out_out = showtime + " " + time_out
            # else:
            time_in_in = dates + " " + time_in
            time_out_out = dates + " " + time_out

            print(
                dates,
                time_in,
                time_out,
                positions,
                desc,
                salary,
                "ddddddddddaaaaaaaaaaaaaaaaaaaaaadddd",
            )

            sr = Shift_Post.objects.latest("id").id + 1000
            Shift_Post.objects.create(
                date=dates,
                in_time=time_in_in,
                out_time=time_out_out,
                position_id=positions,
                text_field=desc,
                wages=salary,
                employee=usr,
                serial_no=sr,
            )
        messages.success(request, "Successfully ! New Shift Post Created")

        return redirect("/manage/shift/")
    else:
        now = datetime.now()

        try:
            us = SocialAccount.objects.get(user_id=request.user.id)
            u = User.objects.get(id=us.user_id)
            u.roll = "employer"
            u.fname = u.first_name
            u.lname = u.last_name
            u.save()
            if u.company_profile_status == False:
                messages.error(request, "Please Fill Your Company Profile ")
                return redirect("/profile/company-profile/" + u.slug)
            else:
                pass
        except:

            return render(
                request,
                "employer/emp_pages/postCreate.html",
                {"number": no_list, "category": obj, "now": now},
            )
    # except:
    #     messages.error(request, "Some thing went wrong")
    #     return render(
    #         request,
    #         "employer/emp_pages/postCreate.html",
    #         {"number": no_list, "category": obj},
    #     )

    return render(
        request,
        "employer/emp_pages/postCreate.html",
        {"number": no_list, "category": obj, "now": now},
    )


# if val == 'accepted':
#                         obj = Shift_Post.objects.filter(employee=usr).filter(
#                             accepted=True, status=True).order_by('-id')
#                         print(obj)
#                         result_obj = paginat.paginate_queryset(obj, request)

#                         sez = ShiftSerialize(result_obj, many=True)

#                 elif val=='completed':
#                         obj=Shift_Post.objects.filter(employee=usr).filter(completed=True,status=True).order_by('-id')
#                         print(obj)
#                         result_obj=paginat.paginate_queryset(obj,request)
#                         sez=ShiftSerialize(result_obj,many=True)
#                 elif val=='pending':
#                         obj=Shift_Post.objects.filter(employee=usr).filter(pending=True,status=True).order_by('-id')
#                         print(obj)
#                         result_obj=paginat.paginate_queryset(obj,request)
#                         sez=ShiftSerialize(result_obj,many=True)
#                 elif val=='new_shift':
#                         obj=Shift_Post.objects.filter(employee=usr,status=True).exclude(completed=True).exclude(pending=True).exclude(accepted=True).order_by('-id')
#                         print(obj)
#                         result_obj=paginat.paginate_queryset(obj,request)
#                         sez=ShiftSerialize(result_obj,many=True)


def delete_post(request, id):
    obj = Shift_Post.objects.get(id=id)
    obj.delete()
    messages.error(request, "Post Is deleted Successfully !!!! ")
    return redirect("/manage/shift/")


@login_required(login_url="/login/")
def manage_shift(request):
    usr = request.user
    newpost = (
        Shift_Post.objects.filter(employee=usr)
        .exclude(completed=True)
        .exclude(accepted=True)
    )
    Accepted_shift = (
        Shift_Post.objects.filter(employee=usr, accepted=True, status=True)
        .exclude(pending=True)
        .exclude(completed=True)
    )
    print(Accepted_shift, "----------------------")
    completed_shift = (
        Shift_Post.objects.filter(employee=usr)
        .filter(completed=True, status=True)
        .order_by("-id")
    )

    pending_shift = (
        Shift_Post.objects.filter(employee=usr, pending=True, status=True)
        .exclude(completed=True)
        .exclude(accepted=True)
    )

    print(newpost, "ddddddddddddddddddddddddddddd")

    page = request.GET.get("page", 1)
    paginator = Paginator(newpost, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # page = request.GET.get("page", 1)
    # paginator = Paginator(Accepted_shift, 2)
    # try:
    #     users = paginator.page(page)
    # except PageNotAnInteger:
    #     users = paginator.page(1)
    # except EmptyPage:
    #     users = paginator.page(paginator.num_pages)

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

        return render(
            request,
            "employer/emp_pages/manage-shifts.html",
            {
                "newpost": newpost,
                "obj": Accepted_shift,
                "users": users,
                "completed": completed_shift,
                "obj3": pending_shift,
            },
        )
    return render(
        request,
        "employer/emp_pages/manage-shifts.html",
        {
            "newpost": newpost,
            "Accepted_shift": Accepted_shift,
            "users": users,
            "completed": completed_shift,
            "pending_shift": pending_shift,
        },
    )


# def time_sheet(request):

#     return render(request, "employer/emp_pages/time-sheet.html")


def sorting_manage_shift(request):
    if request.method == "GET":
        sorting_data = request.GET.get("sorts")
        print("fffffffffffffffffffffffff")
        tab = request.GET.get("tab")
        print(tab, "hiyghuiy9uy78uy78")
        print(sorting_data)
        if int(tab) == 1:
            fetch_data = (
                Shift_Post.objects.filter(employee=request.user, date=sorting_data)
                .exclude(accepted=True)
                .exclude(pending=True)
                .exclude(completed=True)
            )
            print(fetch_data, "ffffffffffffffffffffffffffff")
        elif int(tab) == 2:
            fetch_data = (
                Shift_Post.objects.filter(
                    employee=request.user, accepted=True, date=sorting_data
                )
                .exclude(pending=True)
                .exclude(completed=True)
            )
        elif int(tab) == 3:
            fetch_data = (
                Shift_Post.objects.filter(
                    employee=request.user, pending=True, date=sorting_data
                )
                .exclude(accepted=True)
                .exclude(completed=True)
            )
        else:
            fetch_data = (
                Shift_Post.objects.filter(
                    employee=request.user, completed=True, date=sorting_data
                )
                .exclude(accepted=True)
                .exclude(pending=True)
            )
        print("accepted_fetch_data", fetch_data)

        return render(
            request,
            "employer/emp_pages/filter_manage_shift.html",
            {"accepted_fetch_data": fetch_data},
        )

        #  "accepted_fetch_data": list(accepted_fetch_data), 'pending_fetch_data': list(pending_fetch_data)}, status=200)
    return JsonResponse(
        {"status": "error", "message": "No fetch_data  Successfully !!!!"}, status=404
    )


def search_sorting_manage_shift(request):
    if request.method == "POST":
        data = request.POST.get("s")
        tab = request.POST.get("tab")
        print(tab, "hiyghuiy9uy78uy78")
        print(data, "fffffffffffffffffffffff")
        try:
            if int(tab) == 1:
                fetch_data = (
                    Shift_Post.objects.filter(
                        employee=request.user, applicant_id__fname__icontains=data
                    )
                    .exclude(accepted=True)
                    .exclude(pending=True)
                    .exclude(completed=True)
                )

            elif int(tab) == 2:
                fetch_data = (
                    Shift_Post.objects.filter(
                        employee=request.user,
                        accepted=True,
                        applicant_id__fname__icontains=data,
                    )
                    .exclude(pending=True)
                    .exclude(completed=True)
                )
            elif int(tab) == 3:
                fetch_data = (
                    Shift_Post.objects.filter(
                        employee=request.user,
                        pending=True,
                        applicant_id__fname__icontains=data,
                    )
                    .exclude(completed=True)
                    .exclude(accepted=True)
                )
            else:
                fetch_data = (
                    Shift_Post.objects.filter(
                        employee=request.user,
                        completed=True,
                        applicant_id__fname__icontains=data,
                    )
                    .exclude(pending=True)
                    .exclude(accepted=True)
                )

        except:
            messages.error(request, "Somethig Is Worng")
            return redirect("/manage/shift/")
        return render(
            request,
            "employer/emp_pages/search_manage_shift.html",
            {"accepted_fetch_data": fetch_data},
        )
    return JsonResponse(
        {"status": "error", "message": "No fetch_data  Successfully !!!!"}, status=404
    )


from django.db.models import CharField, Value


def time_sheet(request):
    user_list = User.objects.filter(roll="applicant")

    position = Category.objects.all()

    # try:
    submit_obj = TimeSheet.objects.filter(
        submit_status=True, status=3, employee=request.user
    )

    approve_obj = TimeSheet.objects.filter(
        submit_status=True,
        status=1,
        employee=request.user,
    )
    get = []
    # time=[]
    for i in approve_obj:
        img = i.applicant_id
        get_img = ApplicantDeatails.objects.get(user_id=img)
        get.append(get_img)
        time_in = i.time_in
        time_out = i.time_out
        d = i.date
        x = datetime.combine(d, time_in)
        y = datetime.combine(d, time_out)
        t = y - x
        i.t = t
        i.rating = i.rating

        # print(t, "pppppppppppppppppppppppppppppppppppppp")
    #     ob = approve_obj.annotate(date_diff=Value(t))
    #     print(ob.date_diff, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    # print(approve_obj.values(), "ggggggggggggggggggggggggggggggggggggggg")

    # delta = datetime.combine(date.today(), time_in) - datetime.combine(
    #     date.today(), time_out
    # )
    # delta_hours = delta.days * 24 + delta.seconds / 3600.0

    query_obj = TimeSheet.objects.filter(
        submit_status=True, status=2, employee=request.user
    )

    try:
        us = SocialAccount.objects.get(user_id=request.user.id)
        u = User.objects.get(id=us.user_id)
        u.roll = "employer"
        u.fname = u.first_name
        u.lname = u.last_name
        u.save()

        if u.company_profile_status == False:
            messages.error(request, "Please Fill Your Company Profile ")
            return redirect("/profile/company-profile/" + u.slug)
        else:
            pass
    except:
        return render(
            request,
            "employer/emp_pages/time-sheet.html",
            {
                "submit": submit_obj,
                "approve": approve_obj,
                "query": query_obj,
                "user": user_list,
                "position": position,
                
            },
        )
    # except:
    #     return HttpResponse("ddddddddddddddddddddddd")
    return render(
        request,
        "employer/emp_pages/time-sheet.html",
        {
            "submit": submit_obj,
            "approve": approve_obj,
            "query": query_obj,
            "user": user_list,
            "position": position,
            "get_img": get,
        },
    )


@login_required(login_url="/login/")
def timeSheetFilter(request):
    usr = request.user
    tab = request.GET.get("tab")
    user = request.GET.get("user")
    date = request.GET.get("date")
    position = request.GET.get("position")
    rate = request.GET.get("rate")
    print(tab, tab, user, date, position, rate, "************")
    all_obj = TimeSheet.objects.filter(submit_status=True)
    if tab == "1":
        try:

            a = datetime.fromisoformat(date)
            submit_obj = all_obj.filter(status=3).filter(
                Q(date__lte=a)
                | Q(applicant_id=int(user))
                | Q(app_position_id=int(position) | Q(rating=rate))
            )
        except:
            submit_obj = None
        print(submit_obj, "SSSSSSSSSSSSSSSSSSSSS")
        return render(
            request,
            "employer/emp_pages/time_sheet_filter.html",
            {"query": submit_obj, "tab": tab},
        )
    if tab == "2":
        try:
            a = datetime.fromisoformat(date)
            # approve_obj=TimeSheet.objects.all()
            approve_obj = all_obj.filter(status=1).filter(
                Q(date__lte=a)
                | Q(applicant_id=int(user))
                | Q(app_position_id=int(position) | Q(rating=rate))
            )

        except:
            approve_obj = None
        print(approve_obj, "###############")
        return render(
            request,
            "employer/emp_pages/time_sheet_filter.html",
            {"query": approve_obj, "tab": tab},
        )
    if tab == "3":
        try:
            a = datetime.fromisoformat(date)
            # query_obj=TimeSheet.objects.all()
            query_obj = all_obj.filter(status=2, employee=request.user).filter(
                Q(date__lte=a)
                | Q(applicant_id=int(user))
                | Q(app_position_id=int(position) | Q(rating=rate))
            )
        except:
            query_obj = None
        print(query_obj, "$$$$$$$$$$$$$$$$$$$$$$$")
        return render(
            request,
            "employer/emp_pages/time_sheet_filter.html",
            {"query": query_obj, "tab": tab},
        )


@login_required(login_url="/login/")
def queryView(request, a):
    usr = request.user
    superusers = User.objects.filter(is_superuser=True)
    count = 0
    for i in superusers:
        count = +1
        admin_user = i
        if count == 1:
            break

    position = Category.objects.all()
    obj = TimeSheet.objects.get(id=a)
    if request.method == "POST":
        query = request.POST.get("query")
        print(query, "dddddddddddddddddddd")
        name = request.POST.get("name")
        print(name, "ddddddddddddddd")
        position = request.POST.get("position")
        print(position, "ddddddddddddddd")

        date = request.POST.get("date")
        print(date, "ddddddddddddddd")

        if query and name and position and date:
            obj.status = 2
            obj.save()
            query_obj = Query.objects.create(
                timesheet=obj,
                employee=usr,
                postion_id=position,
                admin=admin_user,
                date=date,
                name=name,
            )
            msg_obj = QueryMessage.objects.create(
                query=query_obj,
                message=query,
                sender=usr,
                reciver=admin_user,
            )
            messages.success(request, "Successfully ! Submitted Query Form")
            return redirect("/time_sheet_manage/")
        else:

            messages.error(request, "Something is missing")
            return render(
                request,
                "employer/emp_pages/query.html",
                {"obj": obj, "position": position},
            )
    else:
        return render(
            request, "employer/emp_pages/query.html", {"obj": obj, "position": position}
        )


@login_required(login_url="/login/")
def approvedView(request, a):
    ids = a
    usr = request.user
    position = Category.objects.all()
    obj = TimeSheet.objects.get(id=ids)
    if request.method == "POST":
        review = request.POST.get("query")
        name = request.POST.get("name")
        position = request.POST.get("position")
        date = request.POST.get("date")
        rate = request.POST.get("demo")
        if review and name and position and date and rate:
            obj.approve_date = date
            obj.approved_by = name
            obj.employee_review = review
            obj.emp_position_id = position
            obj.rating = rate
            obj.status = 1
            obj.resolve_status = 1
            obj.save()
            messages.success(request, "Successfully ! approved Timesheet Form")
            return redirect("/time_sheet_manage/")
        else:
            messages.error(request, "Something is missing")
            return render(
                request,
                "employer/emp_pages/approve.html",
                {"obj": obj, "position": position},
            )
    else:
        return render(
            request,
            "employer/emp_pages/approve.html",
            {"obj": obj, "position": position},
        )


@login_required(login_url="/login/")
def timeSheetDetails(request):
    ids = request.GET.get("timesheet_id")
    usr = request.user
    obj = TimeSheet.objects.get(id=int(ids))
    qurey_obj = Query.objects.get(timesheet=obj)
    query_msg = QueryMessage.objects.filter(query=qurey_obj).order_by("-create_at")[:2]
    # try:
    #     obj=TimeSheet.objects.get(id=int(ids))
    #     qurey_obj=Query.objects.get(timesheet=obj)
    #     query_msg=QueryMessage.objects.filter(query=qurey_obj).order_by('-create_at')[:2]

    # except:
    #     obj=None
    name = usr.fname + " " + usr.lname
    position = usr.position

    date == obj.date
    in_time = obj.time_in
    out_time = obj.time_out

    data_obj = {
        "name": name,
        "position": position,
        "date": date,
        "in_time": in_time,
        "out_time": out_time,
        "message": query_msg,
    }
    print(data_obj)
    return JsonResponse(data_obj)

    # r = q.id
    # data = QueryMessage.objects.filter(query_id=r)


def admin_reply_in_view_query(request, id):
    try:
        q = Query.objects.get(timesheet_id=id)
        print(id)
        details = QueryMessage.objects.filter(query_id=q.id)
        resolve_query = TimeSheet.objects.get(id=id)
        print(resolve_query.resolve_status)

        print(details, "ssssssssssssssssss")
    except:
        q = None
        messages.error(request, "nooooooooooooo")
        return redirect("/admin_reply_in_view_query/" + str(id))
    return render(
        request,
        "employer/emp_pages/view-query.html",
        {"q": q, "details": details, "resolve_query": resolve_query},
    )


def emp_reply(request):
    id = request.user.id
    Q = Query.objects.filter(employee_id=id)
    for i in Q:
        u = i.id
        receiver = i.admin_id
        sender = i.employee_id

    data = QueryMessage.objects.filter(query_id=i.id)
    for i in data:
        id = i.id
        query_id = u
        sender_id = sender
        reciver_id = receiver

    if request.method == "POST":
        emp_reply = request.POST.get("emp_reply")
        print(emp_reply, "ddddddddddddddddddddddddddddddddd")
        save_emp_reply = QueryMessage.objects.create(
            query_id=u,
            sender_id=sender,
            reciver_id=receiver,
            message=emp_reply,
        )

        return HttpResponse(emp_reply)
    return HttpResponse("emp_reply")


def resolve_status(request):
    if request.method == "POST":
        timesheet_id = request.POST.get("timesheet_id")
        status = request.POST.get("resolve_status")

        save_status = TimeSheet.objects.get(id=timesheet_id)
        save_status.resolve_status = status
        save_status.save()
        return JsonResponse(
            {
                "status": "success",
                "message": " Query Resolved !!!!",
                "save_status": save_status.resolve_status,
            },
            status=200,
        )
    return JsonResponse({"status": "error", "message": "No changed !!!!"}, status=404)


def social_login_profile(request):
    obj = User.objects.all()
    obj.delete()

    return HttpResponse("fffffffffffffffff")


def termcondition(request):
    term = ContentManagement.objects.all()
    return render(request, "terms-conditions.html", {"term": term})


from geopy.geocoders import Nominatim


def f(request):
    geolocator = Nominatim(user_agent="geoapiExercises")
    post = "328021"

    location = geolocator.geocode(post)

    return HttpResponse(location)


def chats(request):
    return render(request, "chats.html")


@login_required(login_url="/login/")
def helpChatView(request):
    usr=request.user
    if usr.roll=='employer':
        
        admin_user=User.objects.filter(is_superuser=True)
        c=0
        for i in admin_user:
                c+=1
                if c==1:
                    admin=i
                    break
        
        room_id=f'{admin.id}' + '_room_'+f'{usr.id}'
        try:
                obj = RoomCreate.objects.get(room_name=room_id)
                msg=Message.objects.filter(room=obj)
        
        except:
                obj=RoomCreate.objects.create(f_person=usr,s_person=admin,room_name=room_id)
                msg=None
                room_id=obj.room_name
        
        
        return render(request,'chat_help/liveChat.html',{'user':usr,'room_id':room_id,'msg':msg,'sender':usr.id,'reciver':admin.id})
    else:
        return HttpResponse('admin have not permission')   