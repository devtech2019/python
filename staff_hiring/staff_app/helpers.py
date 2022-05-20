
import sys


from twilio.rest import Client
from django.conf import settings
import random
from staff_app.models import OTP
from django.core.mail import send_mail,EmailMessage
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from django.template.loader import get_template
from xhtml2pdf import pisa
from staff_admin.models import  User
from applicant_web.models import ApplicantDeatails
from django.template.loader import render_to_string
from staff_app.serialize import ApplicantDeatailSerialize,CompanyInfoSerialize,RegisterSerialize

from employee_web.models import *
from_mail=settings.EMAIL_HOST_USER

from_no=settings.TWILIO_NUMBER
sms_sid=settings.TWILIO_ACCOUNT_SID
sms_token=settings.TWILIO_AUTH_TOKEN


def year_list():
    l=list(range(0,15))
    year_range=list()
    for i in l:
            x={'value':i,'label':i}
    
            year_range.append(x)
    return year_range


def vaccinated():
    l=[{'value':1 ,'label':'Fully Vaccinated'}, {'value':2 ,'label':'Not Vaccinated'} ,{'value':3 ,'label':'Partially Vaccinated'}]
    return l


    
  

def haversine(lon1, lat1, lon2, lat2):
   
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r



def sendSMS(user,contact):
    to_contact=contact
    client = Client(sms_sid,sms_token)
    otp=random.randint(1000,9999)
    now = datetime.now()
    user.OTP=otp
    user.OTP_create_at=now
    user.save()
    message = client.messages.create(
                                        body=f'Hi, your test result is {otp} Great job',
                                        from_=from_no,
                                        to='+919783628150' 
                                    )


def sendMail(usr,sub,msg):
    mail=usr.email
    
    send_mail(
                sub,
                msg,
                from_mail,
                [mail],
                fail_silently=False,
                )





def save_data_inObject(date,in_time,out_time,instruct,position,user):
    length=len(date)
    try:
        sr=Shift_Post.objects.latest('id').id+100
    except:
        sr=1000
    for i in range(length):
        obj=Shift_Post()
        obj.date=date[i]
        obj.in_time=in_time[i]
        obj.out_time=out_time[i]
        obj.position_id=int(position[i])
        obj.text_field=instruct[i]
        print(sr+i+1)
        obj.serial_no=sr+i+1
        obj.employee=user
        obj.save()
        print(obj.id)
    return
           




def get_object(lat,lng,user):
    lat1=float(lat)
    lon1=float(lng)
    objs=User.objects.filter(accepted=True,applicant=user)
    l=list()
    for obj in objs:
        t_lat=obj.lat
        t_log=obj.long 
        lat2=t_lat
        lon2=t_log
        a = haversine(lon1, lat1, lon2, lat2)
        radius=80.4672
        if a <= radius:
            l.append(obj)
        else:
            pass
    
    return l


def get_object_postShift(objs,lat,lng):
    lat1=float(lat)
    lon1=float(lng)
    l=list()
    for obj in objs:
        company=User.objects.get(id=obj.employee.id)
        t_lat=company.latitude
        t_log=company.longitude 
        lat2=t_lat
        lon2=t_log
        a = haversine(lon1, lat1, lon2, lat2)
        radius=80.4672
        if a <= radius:
            l.append(obj)
        else:
            pass
    
    return l



def user_details(usr,token,usr_request=None):
    
    
    try:
        position=usr.position.id
        position_name=usr.position.name
        
    except:
        position=None
        position_name=None
    
    try:
        comp=CompanyInfo.objects.get(user=usr)
        comp_sez=CompanyInfoSerialize(comp,context={'request':usr_request})
        
    except:
        comp_sez=None

    try:
        applicant=ApplicantDeatails.objects.get(user=usr)
        app_sez=ApplicantDeatailSerialize(applicant,context={'request':usr_request})
        
    except:
        app_sez=None
        
    if app_sez:
        user={'user_id': usr.pk,
            'email': usr.email,
            'fname':usr.fname,
                'lname':usr.lname,
                'roll':usr.roll,
                'mobile_number':usr.mobile_number,
                'address':usr.address,
                'longitude':usr.longitude,
                'latitude':usr.latitude, 
                'landline':usr.landline,
                'position':position,
                'position_name':position_name,
                'roll':usr.roll,
                
                'push_notification':usr.push_notification,
                'mail_notification':usr.mail_notification,
                'landline number'  :usr.landline,
                'company profile status':usr.company_profile_status,
                'company':usr.company,
                'token':token.key,
                'applcant_info':app_sez.data
                }
        return user
    elif comp_sez:
        user={'user_id': usr.pk,
            'email': usr.email,
            'fname':usr.fname,
                'lname':usr.lname,
                'roll':usr.roll,
                'mobile_number':usr.mobile_number,
                'address':usr.address,
                'longitude':usr.longitude,
                'latitude':usr.latitude, 
                'landline':usr.landline,
                'position':position,
                'position_name':position_name,
                'roll':usr.roll,
                
                'push_notification':usr.push_notification,
                'mail_notification':usr.mail_notification,
                'landline number'  :usr.landline,
                'company profile status':usr.company_profile_status,
                'company':usr.company,
                'token':token.key,
                'company_info':comp_sez.data,
                
                }
        return user
    else:
        user={'user_id': usr.pk,
            'email': usr.email,
            'fname':usr.fname,
                'lname':usr.lname,
                'roll':usr.roll,
                'mobile_number':usr.mobile_number,
                'address':usr.address,
                'longitude':usr.longitude,
                'latitude':usr.latitude, 
                'landline':usr.landline,
                'position':position,
                'position_name':position_name,
                'roll':usr.roll,
                
                'push_notification':usr.push_notification,
                'mail_notification':usr.mail_notification,
                'landline number'  :usr.landline,
                'company profile status':usr.company_profile_status,
                'company':usr.company,
                'token':token.key,
                'company_info':None,
                'applcant_info':None
                }
        return user




def timeSheetValidation(form_data):
    l=['time_in' ,'time_out' ,'break_time' ,'date' ,'authorized_by' ,'position','shift']
    for key in form_data:
        a=key
        if a in l:
            l.remove(a)
    return l



def set_pending():
    now=datetime.today()
    
    obj=Shift_Post.objects.exclude(accepted=True).exclude(pending=True).exclude(completed=True).exclude(status=False)
    obj1=obj.filter(in_time__lte=now)
    for i in obj1:
        i.pending=True
        i.save()
    


def shiftCancelMail(shift):
    applicant=shift.applicant.email
    sub=f'Shift Post() Cancel by Client'
    msg='I have infom that Shift  Post have been  Cancel by client which date is {shift.date} ,In time {shift.in_time} and out time {shift.out_time}'
    
    
    send_mail(
                sub,
                msg,
                from_mail,
                [applicant],
                fail_silently=False,
                )


def html_to_pdf(template_src, context_dict={}):
    html = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None



def send_app_pdf(user):
    try:
        data = ApplicantDeatails.objects.get(user_id=user.id)
    except:
        data=None
    app_user=user
    if data:
            pdf = html_to_pdf('reports/pdf/applicant_details_pdf.html',
                            {'app_user': app_user, 'data': data})
        
    else:
            pdf = html_to_pdf('reports/pdf/applicant_details_pdf.html',
                            {'app_user': app_user})
                      
    msg = EmailMessage("title", "content", to=[app_user.email])
    msg.attach("Report.pdf", pdf, "application/pdf")
    msg.send()



def send_pdf_emp(user):
    u = user.email
    

