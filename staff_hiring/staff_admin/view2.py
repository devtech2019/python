from email import message
from django.conf import settings
from django.core.paginator import Paginator
import json
from django.core import serializers

# from rest_framework import serializers
from django.shortcuts import render
from .models import Message, RoomCreate
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from staff_admin.models import User


@login_required(login_url="/admin/")
def chatView(request):
    userdata = User.objects.all()
    if request.method == "GET":

        current_user = request.user.id
        try:
            user_name = request.GET.get("user_name")
            caller_id = int(request.GET.get("caller_id"))
        except:
            user_name = None
            caller_id = None

        if caller_id != 5:

            usr = User.objects.filter(roll__in=["applicant", "employer"])
            t = serializers.serialize("json", usr, fields=("id", "fname", "lname"))
            message = json.loads(t)
            l = list()

            for i in message:
                id = i["pk"]
                x = i["fields"]
                x["id"] = id
                l.append(x)

            return render(
                request,
                "live_chat/chat.html",
                {"users": l, "f_user": current_user, "userdata": userdata},
            )
        else:
            usr = User.objects.filter(fname__contains=user_name)
            t = serializers.serialize("json", usr, fields=("id", "fname", "lname"))
            message = json.loads(t)
            l = list()
            for i in message:
                id = i["pk"]
                x = i["fields"]
                x["id"] = id
                l.append(x)

            return JsonResponse({"user": l, "f_user": current_user})


def user_chat(request):

    a = request.GET.get("sender")
    b = request.GET.get("reciever")

    room_id = f"{a}" + "_room_" + f"{b}"
    try:
        obj = RoomCreate.objects.get(room_name=room_id)
        msg = Message.objects.filter(room=obj)
        # paginator = Paginator(msg, per_page=15)
        # page_object = paginator.get_page(1)

    except:
        obj = RoomCreate.objects.create(f_person_id=a, s_person_id=b, room_name=room_id)
        msg = None
        # paginator = Paginator(msg, per_page=15)

        # page_object = None
    room = obj.room_name
    try:
        t = serializers.serialize(
            "json", msg, fields=("content", "send_id", "reciever_id", "date_added")
        )
        message = json.loads(t)
        l = list()

        for i in message:
           
            l.append(i["fields"])

        data = {"room": room, "msg": l}

        t = json.dumps(data)
    except:

        l = []
        data = {"room": room, "msg": l}

        t = json.dumps(data)

    return JsonResponse({"data": data})

import os
def testView(request):
    print(os.environ.get("REDIS_HOST", "redis_int"),os.environ.get("REDIS_PORT", 6379))
    return HttpResponse('i think u got something new herer')