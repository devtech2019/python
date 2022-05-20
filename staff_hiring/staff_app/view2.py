
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from staff_admin.models import *
from staff_app.serialize import *
from employee_web import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import api_view
from django.db.models import Q
#from . permission import IsAdmin,IsCompany,IsJobSeeker
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes,permission_classes
import random
import datetime 
from django.conf import settings
from staff_app.helpers import get_object, sendSMS,timeSheetValidation
from twilio.rest import Client

from staff_app.permission import IsCompany,IsJobSeeker
from .helpers import *
from_mail=settings.EMAIL_HOST_USER

from_no=settings.TWILIO_NUMBER
sms_sid=settings.TWILIO_ACCOUNT_SID
sms_token=settings.TWILIO_AUTH_TOKEN
import json
import uuid
from base64 import b64decode
from django.core.files.base import ContentFile   



@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker])
def shiftListByStatus(request):
        if request.method=='GET':
                set_pending()
                usr=request.user
                paginat=PageNumberPagination()
                paginat.page_size=10
                paginat.page_size_query_param='page_size'
                
                try:
                        val=request.GET.get('shift_list')
                       
                except:
                        pass
                now_date=datetime.now()
                # now_date=now_datetime.date()
                # now_time=now_datetime.time()
                
                if val=='booked':
                        print(now_date)
                        ob=Shift_Post.objects.filter(applicant=usr).exclude(in_time__lte=now_date)
                        print(ob)
                        obj=Shift_Post.objects.filter(applicant=usr).filter(accepted=True,status=True).exclude(in_time__lte=now_date).order_by('-create_at')
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ApplcantShiftSerialize(result_obj,many=True,context={'current_user':usr,'request':request})
                
                elif val=='completed':
                        obj=Shift_Post.objects.filter(applicant=usr).filter(completed=True,status=True,accepted=True).order_by('-create_at')
        
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ApplcantShiftSerialize(result_obj,many=True,context={'current_user':usr ,'request':request})
                elif val=='available':
                        obj=Shift_Post.objects.exclude(completed=True).exclude(accepted=True).exclude(pending=True).exclude(status=False).exclude(time_sheet=True).order_by('-create_at')
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ApplcantShiftSerialize(result_obj,many=True,context={'current_user':usr,'request':request})

                elif val=='timesheet':
                        
                        
                        
                        obj=Shift_Post.objects.filter(applicant=usr).filter(accepted=True,status=True).filter(in_time__lte=now_date).order_by('-create_at')
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ApplcantShiftSerialize(result_obj,many=True,context={'current_user':usr,'request':request})

                else:
                        return Response({
                                'status':0,
                                'message':'Please send correct key',
                                'data':[],
                                                
                                })

                t=sez.data
                response=paginat.get_paginated_response(t)
                response.data['message']='data fetch succsfully'
                response.data['status']=1
                return Response(response.data)



@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker])
def shiftBooking(request):
        if request.method=='GET': 
                id=request.GET.get('id')
                usr=request.user
                now_date=datetime.now()
                a=json.loads(id)
                try:
                        shift_obj=Shift_Post.objects.get(id=a)
                except:
                        return Response({
                                'status':1,
                                'message':'Successfully ! id does not exist ',
                                'data':[]
                                                
                                })
                try:
                        check_time=TimeSheet.objects.get(shift=shift_obj)
                except:
                        emp_obj=shift_obj.employee
                        time_obj=TimeSheet.objects.create(applicant=usr,shift=shift_obj,employee=emp_obj)
                        
                if a:   
                        shift_obj.accepted=True
                        shift_obj.applicant=usr
                        shift_obj.save()
                        emp_user=shift_obj.employee
                        try:
                               send_app_pdf(emp_user)
                        except:
                                pass
                        return Response({
                                'status':1,
                                'message':'Successfully ! shift booked',
                                'data':[]
                                                
                                })
                else:
                        return Response({
                                'status':1,
                                'message':'Successfully ! something is wrong ',
                                'data':[]
                                                
                                })




@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker])
def shiftBookingCancel(request):
        if request.method=='GET':
        
                shift_id=request.GET.get('shift_id')
                ids=json.loads(shift_id)
                try:
                        obj=Shift_Post.objects.get(id=ids)
                except:
                        return Response({
                                'status':0,
                                'message':'shift id does not exist',
                                'data':[]
                                                
                                })

                obj.accepted=False
                obj.save()



                return Response({
                                'status':1,
                                'message':'Successfully ! shift Cancel',
                                'data':[]
                                                
                                })






@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def applicantDetails(request):
        if request.method=='POST':
                usr=request.user
                data=request.data
                print(request.data)
                print(request.FILES,'-----------')
                try:
                        
                        vaccinate=request.data['vaccinated']
                        x={1:'Fully Vaccinated', 2:'Not Vaccinated' ,3:'Partially Vaccinated'}
                        z=x[int(vaccinate)]
                except:
                        z=None
              
                try:
                        img=request.FILES.get('image')
                        print(img,"fffffffffffffffffffffff")
                except:
                        img=None
                
                try:
                        
                        app_obj=ApplicantDeatails.objects.get(user=usr)
                        token, created = Token.objects.get_or_create(user=usr)
                        user_info=user_details(usr,token,usr_request=request)
                        return Response({
                                'status':0,
                                'message':'User Already Update details',
                                'data':user_info})
                except:

                        sez=ApplicantDeatailSerialize(data=data,context={'request':request})
                        token, created = Token.objects.get_or_create(user=usr)
                        
                        if sez.is_valid(raise_exception=False):
                                sez.save(user=usr,vaccinated=z,image=img)
                                
                                token, created = Token.objects.get_or_create(user=usr)
                                
                                user_info=user_details(usr,token)
                                try:
                                        obj=User.objects.get(id=usr.id)
                                        obj.company_profile_status=True
                                        obj.save()
                                except:
                                        pass
                                return Response({
                                        'status':1,
                                        'message':'Successfully ! update data',
                                        'data':user_info
                                                        
                                        })
                        else:   
                                
                                for i in sez.errors:
                                        a=0
                                        l=sez.errors[i]
                                        s=f'{i}-{l[0]}'
                                        a+=1
                                        if a==1:
                                                response = {
                                                'status': 0,
                                                'message':s,

                                                'data': []
                                                        }

                                return Response(response)



@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def shift_details(request):
        if request.method=='GET':
                a=request.GET.get('id')
                usr=request.user
                try:
                        obj=Shift_Post.objects.get(id=a)
                except:
                        return Response({
                                'status':0,
                                'message':'Shift POST does not exist',
                                'data':[],
                                                
                                })
                sez=ShiftDetailSerialize(obj,context={'current_user':usr})
                return Response({
                                'status':1,
                                'message':'Successfully ! fatch data',
                                'data':sez.data,
                                                
                                })




@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def timeSheet(request):
        if request.method=='GET':
                usr=request.user
                obj=Shift_Post.objects.filter(applicant=usr,accepted=True,time_sheet=False)
                sez=TimeSheetSerialize(obj,many=True)
                return Response({
                                'status':1,
                                'message':'Successfully  dsds! fatch data',
                                'data':sez.data
                                                
                                })

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def submitTimeSheet(request):
        if request.method=='POST':
                usr=request.user
                data=request.data
                
                
                id=request.data['shift']
                shift_id=json.loads(id)

                print(data)
                try:
                        obj=TimeSheet.objects.get(shift_id=shift_id)
                except:
                        return Response({
                                'status':0,
                                'message':'Shift id does not  exist',
                                'data':[]
                                })
                if obj.submit_status:
                        return Response({
                                'status':0,
                                'message':'Already ! submit Time Sheet',
                                'data':[]
                                })

                sez=TimeSheetSubmitSerialize(instance=obj,data=data,context={'request':request})
                if sez.is_valid():
                        sez.save(submit_status=True)
                        obj.shift.time_sheet=True
                        obj.save()
                        return Response({
                                'status':1,
                                'message':'Successfully! data update',
                                'data':sez.data
                                                
                                })
                else:
                        for i in sez.errors:
                                a=0
                                l=sez.errors[i]
                                s=f'{i}-{l[0]}'
                                a+=1
                                if a==1:
                                        response = {
                                        'status': 0,
                                        'message':s,

                                        'data': []
                                                }

                        return Response(response)




@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def timeSheetStatus(request):
        if request.method=='GET':
                usr=request.user
                print(usr.id)
                obj=TimeSheet.objects.filter(user=usr,submit_status=True)
                sez=TimeSheetStatus(obj,many=True)
                return Response({
                                        'status':1,
                                        'message':'Successfully! fatch',
                                        'data':sez.data
                                                        
                                        })


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def postListForTimeSheet(request):
        usr=request.user

        obj=Shift_Post.objects.filter(applicant=usr,completed=False,time_sheet=False)
        sez=ApplcantShiftSerialize(obj,many=True,context={'current_user':usr})
        return Response({
                                        'status':1,
                                        'message':'Successfully! Fatch data',
                                        'data':sez.data
                                                        
                                        })








@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def likeShift(request):
        if request.method=='GET':
                usr=request.user
                try:
                        id=request.GET.get('shift_id')
                except:
                        return Response({
                                        'status':0,
                                        'message':'Please Send Correct Send Key and Value',
                                        'data':[]
                                                        
                                        })
                shift_id=json.loads(id)
                try:
                        obj=ShiftLike.objects.get(shift=shift_id)
                except:
                        obj=ShiftLike.objects.create(user=usr,shift_id=shift_id)
                if obj.like:
                        obj.delete()
                else:
                        obj.like=True
                        obj.save()
                obj1=obj.shift
                sez=ApplcantShiftSerialize(obj1,context={'current_user':usr})
                return Response({
                                        'status':1,
                                        'message':'Successfully! Add Post in Your Favorite List',
                                        'data':sez.data
                                                        
                                        })

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsJobSeeker]) 
def favoriteList(request):
        if request.method=='GET':
                usr=request.user
                paginat=PageNumberPagination()
                paginat.page_size=10
                paginat.page_size_query_param='page_size'
                try:
                        obj=ShiftLike.objects.filter(user=usr)
                except:
                        obj=None
                if obj:
                        l=list()
                        for i in obj:
                                l.append(i.shift)
                        
                        result_obj=paginat.paginate_queryset(l,request)
                        sez=ApplcantShiftSerialize(result_obj,many=True,context={'current_user':usr})
                        # sez=ApplcantShiftSerialize(l,many=True,context={'current_user':usr})
                        t=sez.data
                        response=paginat.get_paginated_response(t)
                        response.data['message']='data fetch succsfully'
                        response.data['status']=1
                        return Response(response.data)
                else:
                        return Response({
                                                'status':1,
                                                'message':'Not availbler any list ',
                                                'data':[]
                                                                
                                                })

