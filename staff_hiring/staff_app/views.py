
import json
from datetime import datetime
from datetime import datetime, date

from datetime import timedelta
from urllib import response
from rest_framework import serializers 
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from staff_admin.models import *
from staff_app.serialize import *
from employee_web import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from applicant_web.models import ShiftLike

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
from staff_app.helpers import get_object, sendSMS,shiftCancelMail,send_app_pdf,user_details,set_pending
from twilio.rest import Client
from staff_app.helpers import save_data_inObject,sendMail,year_list,vaccinated
from staff_app.permission import IsCompany,IsJobSeeker,CommonUser
from_mail=settings.EMAIL_HOST_USER

from_no=settings.TWILIO_NUMBER
sms_sid=settings.TWILIO_ACCOUNT_SID
sms_token=settings.TWILIO_AUTH_TOKEN
#Create your views here.

def app_pdf(request):
        return render(request,"reports/pdf/app_pdf.html")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getTraining(request):
        if request.method=='GET':
                print('aysuh gupta--------------')
                obj=Training.objects.all()
                sez= TraningSerialize(obj,many=True)
                response={
                'status':1,
                'data':sez.data,
                'message':'Successfully ! fatch data',
                        }
                return Response(response)
                




@api_view(['GET'])
def countryView(request):
    if request.method=='GET':
        obj=Country.objects.all()
        sez=CountrySerialize(obj,many=True)
        response={
            'status':1,
            'data':sez.data,
            'message':'Successfully ! fatch data',
        }
        return Response(response)


@api_view(['GET'])
def cityView(request):
    if request.method=='GET':
        obj=Cities.objects.all()
        sez=StateSerialize(obj,many=True)
        response={
            'status':1,
            'data':sez.data,
            'message':'Successfully ! fatch data',
        }
        return Response(response)


@api_view(['GET'])
def stateView(request):
    if request.method=='GET':
        ids=request.GET.get('country_id')
        obj=States.objects.filter(country_id=ids)
        sez=StateSerialize(obj,many=True)
        response={
            'status':1,
            'data':sez.data,
            'message':'Successfully ! fatch data',
        }
        return Response(response)



@api_view(['GET'])
def appIntro(request):
        if request.method=='GET':
                obj=AppWebIntro.objects.all()
                sez=AppIntroSerialize(obj,many=True,context={'request':request})
                response={
                'status':1,
                'data':sez.data,
                'message':'Successfully ! fatch data',
                }
                return Response(response)

@api_view(['GET'])
def cms_page(request):
        if request.method=='GET':
                try:
                        val=request.GET.get('cms_key')
                        cms_data=ContentManagement.objects.get(slug=val)
                        
                except:
                         response={
                        'status':0,
                        'data':[],
                        'message':'Successfully ! please fill correct key and value',
                         }
                         return Response(response)
              
                sez=CMSSerialize(cms_data)
                response={
                'status':1,
                'data':sez.data,
                'message':'Successfully ! fatch data',
                }
                return Response(response)




@api_view(['GET'])
def aboutUs(request):
        if request.method=='GET':
                try:
                        obj=AboutUs.objects.all()
                except:
                        obj=None
                print(obj)
                sez=AboutUsSerialize(obj,many=True,context={'request':request})
                response={
                'status':1,
                'data':sez.data,
                'message':'Successfully ! fatch data',
                }
                return Response(response)

@api_view(['GET'])
def yearList(request):
        l=year_list()
       
        
        response={
                'status':1,
                'data':l,
                'message':'Successfully ! fatch data',
                }
        return Response(response)


@api_view(['GET'])
def vaccinaList(request):
        
        l=vaccinated()
        response={
                'status':1,
                'data':l,
                'message':'Successfully ! fatch data',
                }
        return Response(response)

@csrf_exempt
@api_view(['GET'])
def getBooster(request):
        if request.method=='GET':
                l=list(range(0,8))
                booster_range=list()
                for i in l:
                        x={'id':i,'label':i}
                
                        booster_range.append(x)
                booster=json.dumps(booster_range)
                return Response({
                                'status':1,
                                'message':'Successfully ! Fetch data ',
                                'data':booster_range
                                                
                                })

@api_view(['POST'])
def registerEmp(request):
    if request.method=='POST':
        
            
        try:
                year=request.data['exp_year']
                
        except:
                year=None
                
        try:
               
                role=request.data['roll']
        except:
                pass
                response={
                'status':0,
                'data':[],
                'message':{'roll':'Field is Required'},
                }
                return Response(response)


        sez=RegisterSerialize(data=request.data)
        if sez.is_valid(raise_exception=False):
                sez.save(roll=role)
                id=sez.data['id']

                usr=User.objects.get(id=id)
                if year:
                        usr.exp_year=year
                        usr.save()
                else:
                        pass
                token, created = Token.objects.get_or_create(user=usr)
                
                
             
                #     sendSMS(usr) send sms
                s=request.build_absolute_uri()
                url = s+f'/mail_confirm/{usr.id}'
                email=usr.email
                # mail_obj=TemplateManagemnet.objects.get(slug='confirm_email')
                sub='just testing purpose'
                msg=f'if you getting so say thank finally i got it {url}'
                print(msg)
                # t=strip_tags(msg)
                # message=t.replace('LINK',f'{url}')
                
                send_mail(
                                sub,
                msg,
                from_mail,
                [email],
                fail_silently=False,
                )
                # sez.data['Token']=token
                response={
                'status':1,
                'data':sez.data,
                'TOKEN':str(token),
                'message':'Employee registration successful',
                        }
                return Response(response)
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
        if request.method=='GET':
                usr=request.user
                sez=RegisterSerialize(usr)
                response={
                                        'status':1,
                                        'message':'Successfully ! data fatch ',
                                        'data':sez.data
                                        }
                return Response(response) 



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def changePassword(request):
        if request.method=='POST':
                usr=request.user
                sez=ChangePassSerialize(data=request.data)
                if sez.is_valid(raise_exception=False):
                        old=sez.validated_data.get('old_password')
                        new=sez.validated_data.get('new_password')
                        if usr.check_password(old)==True:
                                usr.set_password(new)
                                usr.save()
                                response={
                                        'status':1,
                                        'data':sez.data,
                                        'message':'Successfully ! update  password ',
                                        }
                                return Response(response)
                        else:
                             response={
                                        'status':0,
                                        'message':'old password does not match',
                                        'data':[]
                                        }
                             return Response(response)   

@csrf_exempt
@api_view(['POST'])
def forgetPassword(request):
        if request.method=='POST':
                try:
                        email=request.data['email']
                        obj1=User.objects.get(email=email)
                except:
                        email=None
                        obj1=None
                try:
                        contact=request.data['contact']
                        obj=User.objects.get(email=email)
                except:
                        contact=None
                        obj=None
                if email and obj1:
                        otp=random.randint(1000,9999)
                        now=datetime.datetime.now()
                        obj1.OTP=otp
                        obj1.OTP_create_at=now
                        obj1.save()
                        sub='opt send message'
                        msg=f'otp is valid few second{otp}'
                        sendMail(obj1,sub,msg)
                        response={
                                        'status':1,
                                        'message':'Successfully ! send OTP in register mail id',
                                        'data':[]
                                        }
                        return Response(response) 

                elif contact and obj:
                        sendSMS(obj,contact)
                        response={
                                        'status':1,
                                        'message':'Successfully ! send OTP user  register mobile number',
                                        'data':[]
                                        }
                        return Response(response) 
                else:
                        response={
                                        'status':0,
                                        'message':'please fill correct details',
                                        'data':[]
                                        }
                        return Response(response) 


@csrf_exempt
@api_view(['POST'])
def OTP_verified(request):
        if request.method=='POST':
                try:
                        otp=request.data['OTP']
                      
                except:
                        response={
                                        'status':0,
                                        'message':'please fill OTP',
                                        'data':[]
                                        }
                        return Response(response) 
                try:
                        mail=request.data['email']
                        
                        obj=User.objects.get(email=mail)
                        
                        db_otp=obj.OTP
                       
                        
                except:
                        mail=None
                        db_otp=None
                try:
                        contact=request.data['contact']
                        obj1=User.objects.get(mobile_number=contact)
                        db_otp1=obj1.OTP
                       
                        
                except:
                        contact=None
                        db_otp1=None
                
                l=[db_otp1,db_otp]
                print(l)
                if otp in l:
                        response={
                                        'status':1,
                                        'message':'Successfully ! verified OTP',
                                        'data':[]
                                        }
                        return Response(response) 
                else:
                        response={
                                        'status':0,
                                        'message':'OTP does not match',
                                        'data':[]
                                        }
                        return Response(response)

                
                        




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([CommonUser])
def UserProfileUpdate(request):
        if request.method=='POST':
                data=request.data
                usr=request.user

                sez=ProfileUpdateSerialize(instance=usr,data=data,context={'user':usr})
                if sez.is_valid(raise_exception=False):
                        sez.save()
                        response={
                                        'status':1,
                                        'message':'Successfully ! update profile',
                                        'data':sez.data
                                        }
                        return Response(response) 
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








class CustomAuthToken(ObtainAuthToken):
    
    
    def post(self, request, *args, **kwargs):
        
        # request.data._mutable = True
        # request.data['username'] = request.data['username'].lower()
       
        try:
                fcm_token=request.data['fcm_token']
        except:
                token=None
        try:
                device=request.data['device']
        except:
                device=None

        try:    
                
                mail=request.data['username']

              

                users = User.objects.get(Q(username__iexact=mail) | Q(email__iexact=mail))
                user_active=users.is_active
                if user_active==False:
                        return Response({
                        'status':0,
                        'message':'Your account is suspended! Please contact admin user',
                        'data':[],
                        
                        })

                else:
                        pass
        except:
                pass
        
        
       

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        
        try:
                serializer.is_valid(raise_exception=False)
        except:
                return Response({
            'status':0,
            'message':'Please enter correct login credentials',
            'data':[],
            
        })
        try:
                user = serializer.validated_data['user']
        except:
                return Response({
                'status':0,
                'message':'Please fill right crendatials',
                'data':[]
                
                                   
                })
        # if token:
        #         fcm_token(user,token,device)

        if user.email_verified==True:
                token, created = Token.objects.get_or_create(user=user)
                
                data=user_details(user,token)
                #data={'token':token.key, 'user_id': user.pk,'email': user.email}
                return Response({
                'status':1,
                'message':'User login succefully',
                'data':data,
                
                                   
                })
        else:  
                s=request.build_absolute_uri()
                url = s+f'/mail_confirm/{user.id}'
                email=user.email
                # mail_obj=TemplateManagemnet.objects.get(slug='confirm_email')
                sub='just testing purpose'
                msg=f'if you getting so say thank finally i got it {url}'
                print(msg)
                # t=strip_tags(msg)
                # message=t.replace('LINK',f'{url}')
                
                send_mail(
                                sub,
                msg,
                from_mail,
                [email],
                fail_silently=False,
                )

                return Response({
                'status':0,
                'message':'please verify email ',
                'data':[],
                
                })

def mailConfirm(request,a):
    obj=User.objects.get(id=a)
    obj.email_verified=True
    obj.save()
    return HttpResponse('Successfully ! Verified email id ')

@api_view(['POST'])
def contact_noConfirm(request):
        if request.method=='POST':
                sez=OTPSerailize(data=request.data)
                if sez.is_valid():
                        otp=sez.validated_data.get('OTP')
                        contact=sez.validated_data.get('contact')
                        obj=User.objects.get(mobile_number=contact)
                        if obj.OTP==otp:
                                obj.is_active=True
                                obj.save()
                                return Response({
                                'status':1,
                                'message':'Successfully ! verified contact number',
                                'data':[]
                                                
                                })
                        else:
                                return Response({
                                'status':1,
                                'message':'OTP does not match',
                                'data':[]
                                                
                                })

#contact no otp verification
@api_view(['POST'])
def OTP_Verification(request):
        if request.method=='POST':
                sez=OTPSerailize(data=request.data)
                if sez.is_valid():
                        otp=sez.validated_data.get('OTP')
                        contact=sez.validated_data.get('contact')
                        obj=User.objects.get(mobile_number=contact)
                        if '1234'==otp:
                        #if obj.OTP==otp:
                                token, created = Token.objects.get_or_create(user=obj)
                                data=user_details(obj,token)
                                return Response({
                                'status':1,
                                'message':'data fetch succefully',
                                'data':data
                                                
                                })
                        else:
                                return Response({
                                'status':0,
                                'message':'OTP does not match',
                                'data':[],
                                                
                                })
        
@api_view(['POST'])
def mobile_login(request):
        if request.method=='POST':
                no=request.data['contact']
                
                try:
                        obj=User.objects.get(mobile_number=no)
                except:
                        
                        return Response({
                                'status':0,
                                'message':'Mobile no does not register',
                                'data':[],
                        })
                if obj.roll=="applicant":
                        t='8555555'
                        try:
                                sendSMS(obj,t)
                        except:
                                pass
                        return Response({
                                'status':1,
                                'message':'OTP Send Registor Mobile Number!',
                                'data':[],
                                                
                                })
                else:
                        return Response({
                                'status':0,
                                'message':'This Process Only For Applicant User',
                                'data':[],
                        })
                

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsCompany])
def category(request):
        if request.method=='GET':
                
                
                obj=Category.objects.all()
                sez=CategorySerialize(obj,many=True)
                return Response({
                                'status':1,
                                'message':'Successfully ! fetch data',
                                'data':sez.data,
                                                
                                })

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany])
def postShift(request):
        if request.method=='POST':
                usr=request.user
                data=request.data

                try:
                        sr=Shift_Post.objects.latest('id').id+1000
                except:
                        sr=1000
                sez=ShiftPostCreateSerialize(data=data)
                s=sr+1
                if sez.is_valid(raise_exception=False):
                        sez.save(serial_no=s,employee=usr)
                        
                        return Response({
                                'status':1,
                                'message':'Successfully ! fetch data',
                                'data':sez.data,
                                                
                                })
                else:
                        return Response({
                                'status':0,
                                'message':'something is missing ',
                                'data':sez.data,
                                                
                                })



@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany])
def shitfPostList(request):
        
        if request.method=='GET':
                set_pending()
                usr=request.user
                paginat=PageNumberPagination()
                paginat.page_size=10
                
                paginat.page_size_query_param='page_size'
                

                try:
                        val=request.GET.get('post_key')                       
                except:
                        pass
               
                if val=='accepted':
                        obj=Shift_Post.objects.filter(employee=usr).filter(accepted=True,status=True).order_by('-create_at')
                        print(obj)
                        result_obj=paginat.paginate_queryset(obj,request)
                        
                        sez=ShiftSerialize(result_obj,many=True)
                
                elif val=='completed':
                        obj=Shift_Post.objects.filter(employee=usr).filter(completed=True,status=True).order_by('-create_at')
                        print(obj)
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ShiftSerialize(result_obj,many=True)
                elif val=='pending':
                        obj=Shift_Post.objects.filter(employee=usr).filter(pending=True,status=True).order_by('-create_at')
                        
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ShiftSerialize(result_obj,many=True)
                elif val=='new_shift':
                        obj=Shift_Post.objects.filter(employee=usr,status=True).exclude(completed=True).exclude(pending=True).exclude(accepted=True).order_by('-create_at')
                        print(obj)
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=ShiftSerialize(result_obj,many=True)
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
@permission_classes([IsCompany])
def shitfPostCancel(request):
        if request.method=='GET':
                try:
                        id=request.GET.get('shift_id')
                except:
                        return Response({
                                'status':0,
                                'message':'Please enter right key and value',
                                'data':[]
                                                
                                })

                shift_id=json.loads(id)
                try:
                        obj=Shift_Post.objects.get(id=shift_id)
                except:
                        return Response({
                                'status':0,
                                'message':'shift id does not exist',
                                'data':[]
                                                
                                })

                obj.status=False
                obj.save()
                try:
                        shiftCancelMail(obj)
                except:
                        pass
                return Response({
                                'status':1,
                                'message':'Successfully ! shift Cancel',
                                'data':[]
                                                
                                })




@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany])
def shitfPostDelete(request):
        if request.method=='GET':
                shift_id=request.GET.get('id')
                ids=json.loads(shift_id)
                try:
                    obj=Shift_Post.objects.get(id=ids)
                    obj.delete()
                except:
                        return Response({
                                'status':0,
                                'message':'Post Shift does Not exist',
                                'data':[],
                                                
                                })
                return Response({
                                'status':1,
                                'message':'Successfully ! Delete  Shift Post ',
                                'data':[],
                                                
                                })   
        




               

           



@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([CommonUser])  
def set_notifcation(request):
        if request.method=='POST':
                usr=request.user
                obj=User.objects.get(email=usr)
                obj_data=request.data
                sez=SetNotificationSerialize(data=obj_data)
                if sez.is_valid():
                        a=sez.validated_data.get('mail_notification')
                        b=sez.validated_data.get('push_notification')
                        obj.mail_notification=a
                        obj. push_notification=b
                        obj.save()

                        return Response({
                                        'status':1,
                                        'message':'Successfully ! update setting ',
                                        'data':sez.data
                                                        
                                        })



@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany]) 
def employeeDetails(request):
        if request.method=='POST':
                usr=request.user
                data=request.data
                sez=CompanyInfoSerialize(data=data)
                try:
                        obj=CompanyInfo.objects.get(user=usr)
                        return Response({
                                'status':0,
                                'message':'User Already Update details',
                                'data':[],
                                                
                                })
                except:
                                
                        
                        token, created = Token.objects.get_or_create(user=usr)
                        
                        if sez.is_valid(raise_exception=False):
                                sez.save(user=usr)
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
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany]) 
def feedback_emp(request):
         if request.method=='POST':
                usr= request.user
                data=request.data
                sez=FeedbackSerialize(data=data)
                if sez.is_valid(raise_exception=False):
                        sez.save(client=usr)
                        return Response({
                                'status':1,
                                'message':'Successfully ! update feedback',
                                'data':sez.data,
                                                
                                })
                else:
                        return Response({
                                'status':1,
                                'message':'Something ! Is missing',
                                'data':sez.data,
                                                
                                })



@csrf_exempt
@api_view(['POST'])
#@authentication_classes([TokenAuthentication])
# @permission_classes([IsCompany]) 
def enquiry(request):
        if request.method=='POST':
                name=request.data['name']
                try:
                        fname,lname=name.split(' ',1)
                except:
                        fname=name
                        lname=None

                print()
                sez=EnquriSerialize(data=request.data)
                if sez.is_valid(raise_exception=False):
                        sez.save(First_name=fname,Last_name=lname)
                
                        return Response({
                                'status':1,
                                'message':'Successfully  ! send  request',

                                'data':sez.data,
                                                
                                })
                else:
                        return Response({
                                'status':0,
                                'message':'Something ! Is missing',
                                'data':sez.data,
                                                
                                })












@csrf_exempt
@api_view(['POST'])
def newPasswordSet(request):
        if request.method=='POST':
                mail=request.data['email']
                new_password=request.data['password']
                usr=User.objects.get(email=mail)
                if usr:
                        usr.set_password(new_password)
                        usr.save()
                        d={'roll':usr.roll}
                        return Response({
                                        'status':1,
                                        'message':'Successfully  ! reset  password',
                                        'data':d,
                                                        
                                        })
                else:
                        return Response({
                                        'status':0,
                                        'message':'email does not match',
                                        'data':[],
                                                        
                                        })


import time
@api_view(['GET'])
def testview(request):
        if request.method=='GET':
                # obj=Shift_Post.objects.get(id=105)
                # t=datetime.datetime.combine(obj.date,obj.in_time)
                obj1=TimeSheet.objects.all()
                obj1.delete()
                obj2=ApplicantDeatails.objects.all()

                obj2.delete()
                obj=Shift_Post.objects.all()
                obj.delete()
                obj1=TimeSheet.objects.all()
                obj1.delete()
                obj4=User.objects.all()
                obj4.delete()
                # obj3=CompanyInfo.objects.all()
                # obj3.delete()
                obj4=User.objects.all()
                obj4.delete()
                obj5=Query.objects.all()
                obj5.delete()
                obj6=QueryMessage.objects.all()
                obj6.delete()
               
                # except Exception as e:
                #         print('this is timesheet exception')
                
                return Response({
                'status':0,
                'message':'dfdfd',
                'data':[],
                
                })


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany]) 
def submitTimeSheetList(request):
        if request.method=='GET':
                usr=request.user
                
                paginat=PageNumberPagination()
                paginat.page_size=10
                try:
                        timeSheetKey=request.GET.get('timeSheetKey')
                except:
                        return Response({
                                'status':0,
                                'message':'Please Enter Right key and value',
                                'data':[]
                                                
                                })

                if timeSheetKey=='submit':
                        obj=TimeSheet.objects.filter(submit_status=True,employee=usr,status=3)
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=TimeSheetSerialize(result_obj,many=True,context={'request':request})
                elif timeSheetKey=='approved':
                        obj=TimeSheet.objects.filter(status=1,employee=usr)
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=TimeSheetSerialize(result_obj,many=True,context={'request':request})
                        
                elif timeSheetKey=='rejected':
                        obj=TimeSheet.objects.filter(status=2,employee=usr) | TimeSheet.objects.filter(resolve_status=True,employee=usr)
                        result_obj=paginat.paginate_queryset(obj,request)
                        sez=TimeSheetSerialize(result_obj,many=True,context={'request':request})
                
                
                else:
                        return Response({
                                'status':1,
                                'message':'Successfully ! Fetch Data',
                                'data':[]
                                                
                                })
                
                t=sez.data
                response=paginat.get_paginated_response(t)
                response.data['message']='data fetch succsfully'
                response.data['status']=1
                return Response(response.data) 


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany]) 
def timeSheetApprove(request):
        if request.method=='POST':
                usr=request.user
                timesheet_id=json.loads(request.data['timesheet_id'])
                data=request.data
                try:
                      obj=TimeSheet.objects.get(id=timesheet_id)
                except:
                        return Response({
                                'status':0,
                                'message':'TimeSheet id does not match',
                                'data':[]
                                                
                                })
                
                sez=TimeSheetApproveSerializer(instance=obj,data=data)
                if sez.is_valid():
                        sez.save(status=1)
                        x=obj.shift.id
                        print(x,'-----------------')
                        post_obj=Shift_Post.objects.get(id=x)
                        post_obj.completed=True
                        post_obj.update_at=datetime.datetime.now()
                        post_obj.save()

                        return Response({
                                'status':1,
                                'message':'Successfully ! Approved  TimeSheet',
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
@permission_classes([IsCompany]) 
def ApproveTimeSheetDetails(request):
        if request.method=='GET':
                ids=request.GET.get('id')
                try:
                      obj=  TimeSheet.objects.get(id=ids)
                except:
                        return Response({
                                'status':0,
                                'message':'TimeSheet id does not match ',
                                'data':[]
                                                
                                })
                sez=GetTimeShettDetailSerialize(obj,context={'request':request})
                return Response({
                                'status':1,
                                'message':'Successfully ! fetech data ',
                                'data':sez.data
                                                
                                })



@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany]) 
def timeSheetQuery(request):
        if request.method=='POST':
                usr=request.user
                data=request.data
                try:
                        msg=request.data['message']
                        id=request.data['timesheet']
                        
                except:
                        msg=None
                        name=None


                timesheet_id=json.loads(id)
                try:
                        obj=TimeSheet.objects.get(id=int(timesheet_id))
                except:
                        return Response({
                                'status':1,
                                'message':'TimeSheet id does not match !',
                                'data':[]
                                                
                                })
                sez=QuerySerialize(data=data)
                admin_user=User.objects.filter(is_superuser=True)
                c=0
                for i in admin_user:
                        c+=1
                        if c==1:
                         admin=i
                         break
                
                if sez.is_valid():
                        objx=sez.save()
                        
                        
                        msg_query=objx.id
                      
                        QueryMessage.objects.create(query_id=msg_query,message=msg,sender=usr,reciver=admin)
                        obj.status=2
                        x=obj.shift.id
                       
                        post_obj=Shift_Post.objects.get(id=x)
                        post_obj.update_at=datetime.datetime.now()
                        post_obj.save()
                        obj.save()
                        return Response({
                                'status':1,
                                'message':'Successfully ! send Query ',
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
@permission_classes([IsCompany])
def getQuery(request):
        if request.method=='GET':
                timesheet_id=request.GET.get('timesheet_id')
                obj=Query.objects.filter(timesheet_id=int(timesheet_id))
                sez=QueryDetailsSerializer(obj,many=True,context={'request':request})
                return Response({
                                'status':1,
                                'message':'Successfully ! fetech data ',
                                'data':sez.data
                                                
                                })
                

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany])
def sendQuery(request):
        if request.method=='POST':
                usr=request.user
                msg=request.data['message']
                query_id=request.data['query_id']
                admin_user=User.objects.filter(is_superuser=True)
                c=0
                for i in admin_user:
                        c+=1
                        if c==1:
                         admin=i
                         break
                
                obj=QueryMessage.objects.create(message=msg,sender=usr,reciver=admin,query_id=int(query_id))
                return Response({
                                'status':1,
                                'message':'Successfully ! send Query to amdin ',
                                'data':msg
                                                
                                })


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCompany])
def queryResolve(request):
        if request.method=='GET':
                timesheet_id=request.GET.get('timesheet_id')
                obj=TimeSheet.objects.get(id=int(timesheet_id))
                obj.status=1
                obj.resolve_status=True
                obj.save()
                return Response({
                                'status':1,
                                'message':'Successfully ! resolved Query ',
                                'data':[]
                                                
                                })


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([CommonUser])
def getRoomId(request):
        if request.method=='GET':
                usr=request.user
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
                
                
                return Response({
                                'status':1,
                                'message':'Successfully ! fetch room id  ',
                                'data':{'room_id':room_id,'reciver_id':admin.id}
                                                
                                })

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([CommonUser])
def getMessage(request):
        if request.method=='GET':
                paginat=PageNumberPagination()
                paginat.page_size=30
                paginat.page_size_query_param='page_size'
                room_id=request.GET.get('room_id')
                room=RoomCreate.objects.get(room_name=room_id)
                obj=Message.objects.filter(room_id=room).order_by('-id')
                result_obj=paginat.paginate_queryset(obj,request)
                sez=GetMessageSerialize(result_obj,many=True)
                t=sez.data
                response=paginat.get_paginated_response(t)
                response.data['message']='data fetch succsfully'
                response.data['status']=1
                return Response(response.data) 