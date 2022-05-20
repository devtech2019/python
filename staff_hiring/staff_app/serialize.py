

# from .helpers import *
# from .helpers import haversine
from math import radians, cos, sin, asin, sqrt
import json
from rest_framework import serializers
from staff_admin.models import *
from employee_web.models import *
from django.contrib.auth.hashers import make_password
from applicant_web.models import *
from datetime import datetime
from rest_framework.validators import UniqueValidator

from rest_framework import serializers    
from django.core.files.base import ContentFile
import base64
import six
import uuid
from rest_framework.validators import UniqueValidator




def haversine(lon1, lat1, lon2, lat2):
   
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


class Base64ImageField(serializers.ImageField):
    

    def to_internal_value(self, data):
        

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class CountrySerialize(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=['id','name']

class StateSerialize(serializers.ModelSerializer):
    class Meta:
        model=States
        fields=['id','name']

class CitySerialize(serializers.ModelSerializer):
    class Meta:
        model=Cities
        fields=['id','name']




class AppIntroSerialize(serializers.ModelSerializer):
    class Meta:
        model=AppWebIntro
        fields='__all__'
    
    def get_image(self,obj):
                request = self.context.get('request')
                photo_url = obj.url
                return request.build_absolute_uri(photo_url)




    # def validate_email(self, value):
    #             norm_email = value.lower()
    #             if User.objects.filter(email=norm_email).exists():
    #                     raise serializers.ValidationError("This email already exist")
    #             return norm_email



class RegisterSerialize(serializers.ModelSerializer):
    email = serializers.EmailField()
    mobile_number= serializers.CharField()
    # exp_month=serializers.SerializerMethodField()
    # exp_year=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id','fname','lname','landline','company','email','address','latitude','longitude','password','address2',
        
        'city','country','post_code','mobile_number','position','mail_notification','push_notification','exp_year','exp_month']
        extra_kwargs = {'landline': {'required': False},'id':{'read_only':True},'company':{'required': False},'landline': {'required': False},'position': {'required': False},
        'push_notification':{'read_only':True},
        'push_notification': {'read_only':True},
        'lname': {'required': False},
        'exp_year': {'required': False},
        'exp_month':{'required': False},
        'address2':{'required': False}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerialize, self).create(validated_data)

    def validate_email(self, value):
                norm_email = value.lower()
                if User.objects.filter(email=norm_email).exists():
                        raise serializers.ValidationError("This email already exist")
                return norm_email

    def validate_mobile_number(self, value):
        

        if  User.objects.filter(mobile_number__exact=value).exists():
            raise serializers.ValidationError("Mobile Number already exists!")
        
        return value

    def get_exp_month(self,obj):
        x=obj.exp_month
        print(x,'--------')
        if x:
            return int(x)
        else:
            x=None

    def get_exp_year(self,obj):
        x=obj.exp_year
        if x:
            return int(x)
        else:
            x=None

class ProfileUpdateSerialize(serializers.ModelSerializer):
    email = serializers.EmailField()
    mobile_number= serializers.CharField()
    class Meta:
        model=User
        fields=['id','fname','lname','landline','company','email','address','address2','latitude','longitude','mobile_number',
        'city','country','post_code','position','mail_notification','push_notification','roll','image','exp_year','exp_month']
        extra_kwargs = {'landline': {'required': False},'id':{'read_only':True},'company':{'required': False},'landline': {'required': False},'position': {'required': False},
        'push_notification':{'read_only':True},
        'push_notification': {'read_only':True},
        'image': {'required': False},
        'exp_year': {'required': False},
        'lname': {'required': False},
        'roll': {'read_only': True},
        'address2': {'required': False}}

    def validate_mobile_number(self, value):
        usr=self.context.get('user')
        

        if  User.objects.exclude(id=usr.id).filter(mobile_number__exact=value).exists():
            raise serializers.ValidationError("Mobile Number already exists!")
        
        return value

    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super(RegisterSerialize, self).create(validated_data)

    # def validate_email(self, value):
    #             norm_email = value.lower()
    #             if User.objects.filter(email=norm_email).exists():
    #                     raise serializers.ValidationError("This email already exist")
    #             return norm_email

class OTPSerailize(serializers.Serializer):
    contact=serializers.CharField()
    OTP=serializers.CharField()



class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','shift_diffrence','week_hour','leave_day']



class ShiftPostCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model=Shift_Post
        fields=['date','in_time','out_time','text_field','position','break_time','wages']


class ShiftSerialize(serializers.ModelSerializer):
    position=serializers.SerializerMethodField()
    # out_time=serializers.SerializerMethodField()
    # in_time=serializers.SerializerMethodField()
    address=serializers.SerializerMethodField()
    applicant_name=serializers.SerializerMethodField()
    class Meta:
        model=Shift_Post
        fields=['id','date','in_time','out_time','text_field','position','accepted','wages','address','applicant_name']
        extra_kwargs={'id':{'read_only':True},'applicant_name':{'read_only':True}}

    def get_position(self,obj):
        return obj.position.name

    # def get_out_time(self,obj):
    #     x=obj.out_time
        
    #     t=str(x)[:5]
        
    #     return t
    # def get_in_time(self,obj):
    #     x=obj.in_time
        
    #     t=str(x)[:5]
        
        return t
    def get_address(self,obj):
        x=obj.employee.address
        return x

    def get_applicant_name(self,obj):
        try:
            x=obj.applicant.fname
            y=obj.applicant.lname
            z=x+' '+y 
            return z 
        except:
            return None


class EmployeeUserSerialize(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['company','address','city','post_code','mobile_number','fname','lname']


class ApplcantShiftSerialize(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    employee=EmployeeUserSerialize(read_only=True)
    distance = serializers.SerializerMethodField('is_distance')
    company=serializers.SerializerMethodField('is_name')
    is_favorite=serializers.SerializerMethodField()
    timeSheet_status=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()
    name_position=serializers.SerializerMethodField()
    worked_hour=serializers.SerializerMethodField()
    def is_distance(self, obj):

        
        try:
            applicant=self.context.get('current_user')
            
            user_id=obj.employee.id
            lat2=applicant.latitude
            lng2=applicant.longitude
            obj=User.objects.get(id=user_id)
            lat1=obj.latitude
            lng1=obj.longitude
            t=haversine(lat1,lng1,lat2,lng2)
            return t
        except:
            return None
    

    def is_name(sefl,obj):
        client=obj.employee
        return client.company

    

    class Meta:
        model=Shift_Post
        fields=['id','date','distance','company','in_time','out_time','employee','text_field','is_favorite','timeSheet_status','rating','position','name_position','image','worked_hour']

    

    def get_is_favorite(self,obj):
        applicant=self.context.get('current_user')
        try:
            x=ShiftLike.objects.get(shift=obj,user=applicant)
            t=x.like
            return t
        except:
            t=False
            return t

    def get_timeSheet_status(self,obj):
        applicant=self.context.get('current_user')
        try:
            x=TimeSheet.objects.get(shift=obj,applicant=applicant)
            if x.submit_status:
                z=x.status
                y=json.loads(z)
                #x={1:'approve',2:'rejected','3':'pending'}
                x={1:'3',3:'2',2:'4'}
                t=x[y]
                return t
            else:
                t='1'
                return t
        except:
            t=None
            return t

    def get_rating(self,obj):
        try:
            id=obj.id

            objs=TimeSheet.objects.get(shift_id=id)
            rating=objs.rating
            return rating
        except:
            rating=None
            return rating

    def get_name_position(self,obj):
        position_name=obj.position.name     
        return position_name

    def get_image(self,obj):
         
        try:
            app_info=obj.applicant
            obj=ApplicantDeatails.objects.get(user=app_info)
            request = self.context.get('request')
            photo_url = obj.image.url
            return request.build_absolute_uri(photo_url) 
        except:
            t=None
            return t   

    def get_worked_hour(self,shift_obj):
        
        try:
            obj=TimeSheet.objects.get(shift=shift_obj)
            t1=obj.time_in
            t2=obj.time_out
            d=obj.date
            print(t1,t2)
            x=datetime.combine(d,t1)
            y=datetime.combine(d,t2)
            t=y-x
            return str(t)
        except:
            t=None
            return t

# class EmployeeUserSerialize(serializers.ModelSerializer):

#     class Meta:
#         model=User
#         fields=['company','address','city','state','post_code','mobile_number','fname','lname']



class ShiftDetailSerialize(serializers.ModelSerializer):
    employee=EmployeeUserSerialize(read_only=True)
    is_favorite=serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField('is_distance')
    timeSheet_status=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()
    def is_distance(self, obj):
        try:
            applicant=self.context.get('current_user')
            
            user_id=obj.employee.id
            lat2=applicant.latitude
            lng2=applicant.longitude
            obj=User.objects.get(id=user_id)
            lat1=obj.latitude
            lng1=obj.longitude
            t=haversine(lat1,lng1,lat2,lng2)
            return t
        except:
            return None 
    class Meta:
        model=Shift_Post
        fields=['id','date','in_time','out_time','text_field','position','accepted','employee','wages','distance','is_favorite','timeSheet_status','rating']

    def get_is_favorite(self,obj):
        applicant=self.context.get('current_user')
        try:
            x=ShiftLike.objects.get(shift=obj,user=applicant)
            t=x.like
            return t
        except:
            t=False
            return t

    def get_timeSheet_status(self,obj):
        
        try:
            x=TimeSheet.objects.get(shift=obj)
            if x.submit_status:
                z=x.status
                y=json.loads(z)
                #x={1:'approve',2:'rejected','3':'pending'}
                x={1:'3',3:'2',2:'4'}
                t=x[y]
                return t
            else:
                t='1'
                return t
        except:
            t=None
            return t

    def get_rating(self,obj):
        try:
            id=obj.id

            objs=TimeSheet.objects.get(shift_id=id)
            rating=objs.rating
            return rating
        except:
            rating=None
            return rating
       

class ChangePassSerialize(serializers.Serializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField()



class CompanyInfoSerialize(serializers.ModelSerializer):
    class Meta:
        model=CompanyInfo
        fields='__all__'
        extra_kwargs = {'user': {'required': False},'company_name': {'required': False},'user_slug': {'required': False},'about_company': {'required': False},'other': {'required': False}}



class ApplicantDeatailSerialize(serializers.ModelSerializer):
    # image=serializers.SerializerMethodField()
    
    class Meta:
        model=ApplicantDeatails
        fields=['user','image','vaccinated','Mnc_pin','recitation','dob','booster_dose','training','training_start_date','training_end_date']
        extra_kwargs = {'image': {'required': False},'user': {'required': False},'booster_dose': {'required': False}}

    def get_image(self,obj):
                request = self.context.get('request')
                try:
                    photo_url = obj.image
                    obj=photo_url.url
                    return request.build_absolute_uri(obj)
                   
                except:
                    t=None
                    return t


class AvailableShiftSerializer(serializers.ModelSerializer):
    home_name=serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField('is_distance')

    def is_distance(self,obj):
        applicant=self.context['applicant']
        lat1=applicant.latitude
        lng1=applicant.longitude
        user_id=obj.employee.id
        obj=User.objects.get(id=user_id)
        lat2=obj.latitude
        lng2=obj.longitude
        t=haversine(lat1,lng1,lat2,lng2)
        return t
    
    class Meta:
        model=Shift_Post
        # fields='__all__'
        fields=['id','date','in_time','home_name','distance']


    def get_home_name(self,obj):
        obj=obj.employee
        home_name=User.objects.get(id=obj.id).company
        return home_name



class FeedbackSerialize(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields=['rating','applicant','client','review','job_post']
        extra_kwargs = {'client': {'required': False},}



class EnquriSerialize(serializers.ModelSerializer):
    class Meta:
        model=ContactUs
        fields=['email','message','sub']


class Shift_Serialize(serializers.ModelSerializer):
    class Meta:
        model=Shift_Post
        fields=['in_time','out_time','break_time']






    class Meta:
        model=TimeSheet
        fields=['company','date','in_time','out_time','break_time','hour_worked']


class SetNotificationSerialize(serializers.Serializer):
    mail_notification=serializers.BooleanField()
    push_notification=serializers.BooleanField()


class TraningSerialize(serializers.ModelSerializer):
    class Meta:
        model=Training
        fields=['id','training_name']

class AboutUsSerialize(serializers.ModelSerializer):
    class Meta:
        model=AboutUs
        fields=['id','title','image','discripion']
    
    def get_image(self,obj):
                request = self.context.get('request')
                photo_url = obj.url
                return request.build_absolute_uri(photo_url)


class CMSSerialize(serializers.ModelSerializer):
    class Meta:
        model=ContentManagement
        fields=['id','desc','title']



class TimeSheetSubmitSerialize(serializers.ModelSerializer):
    sign_img=Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model=TimeSheet
        fields=['id','time_in','time_out','break_time','authorized_by','app_position','date','applicant_review','shift','sign_img']
        extra_kwargs = {'applicant_review': {'required': False},'authorized_by': {'required': False},'sign_img':{'required': False}}

    def get_sign_img(self,obj):
                request = self.context.get('request')
                photo_url = obj.url
                return request.build_absolute_uri(photo_url)


class TimeSheetSerialize(serializers.ModelSerializer):
    home_name=serializers.SerializerMethodField()
    applicant_name=serializers.SerializerMethodField()
    worked_hour=serializers.SerializerMethodField()
    wages=serializers.SerializerMethodField()
    app_position_name=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model=TimeSheet
        fields=['id','time_in','time_out','break_time','date','home_name','applicant_name','app_position','worked_hour','wages','app_position_name','rating','image']        

    def get_home_name(self,obj):
        try:
            emp_obj=obj.employee
            company=emp_obj.company
            return company
        except:
            return None

    def get_applicant_name(self,obj):
        app_obj=obj.applicant
        fname=app_obj.fname
        lname=app_obj.lname
        full_name=fname+' '+lname
        return full_name
    
    def get_worked_hour(self,obj):
        
        try:
        
            t1=obj.time_in
            t2=obj.time_out
            d=obj.date
            print(t1,t2)
            x=datetime.combine(d,t1)
            y=datetime.combine(d,t2)
            t=y-x
            return str(t)
        except:
            t=None
            return t
        
    def get_wages(self,obj):
        wage=obj.shift.wages
        return wage
    
    def get_app_position_name(self,obj):
        try:
            position_obj=obj.app_position
            position_name=position_obj.name
            return position_name
        except:
            return None

    def get_image(self,obj):
         
        try:
            app_info=obj.applicant
            obj=ApplicantDeatails.objects.get(user=app_info)
            request = self.context.get('request')
            photo_url = obj.image.url
            return request.build_absolute_uri(photo_url) 
        except:
            t=None
            return t   

class TimeSheetApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model=TimeSheet
        fields=['rating','approve_date','approved_by','emp_position','employee_review']
        extra_kwargs = {'employee_review': {'required': False},}

class QuerySerialize(serializers.ModelSerializer):
    class Meta:
        model=Query
        fields=['id','employee','admin','timesheet','postion','date','name']
        extra_kwargs = {'admin': {'required': False},}



class GetTimeShettDetailSerialize(serializers.ModelSerializer):
    position_name=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model=TimeSheet
        fields=['id','date','time_in','time_out','break_time','position_name','app_position','image']


    def get_position_name(self,obj):
        try:
            name=obj.app_position.name
            return name
        except:
            name=None
            return name

    def get_image(self,obj):
         
        try:
            app_info=obj.applicant
            obj=ApplicantDeatails.objects.get(user=app_info)
            request = self.context.get('request')
            photo_url = obj.image.url
            return request.build_absolute_uri(photo_url) 
        except:
            t=None
            return t   



class QueryDetailsSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    user_name=serializers.SerializerMethodField()
    user_position=serializers.SerializerMethodField()
    in_time=serializers.SerializerMethodField()
    out_time=serializers.SerializerMethodField()
    message=serializers.SerializerMethodField()
    postion=serializers.SerializerMethodField()
    query_date=serializers.SerializerMethodField()
    query_status=serializers.SerializerMethodField()
    

    class Meta:
        model=Query
        # fields=['message','sender','reciver','create_at','name','user_name']
        fields=['id','timesheet','date','image','name','message',
        'user_name','user_position','in_time','out_time','postion','query_date','query_status']

    def get_user_name(self,obj):
        fname=obj.timesheet.applicant.fname
        lname=obj.timesheet.applicant.lname
        full_name=fname+' '+lname
        return full_name

    def get_user_position(self,obj):
        position=obj.timesheet.applicant.position.name
        return position

    def get_in_time(self,obj):
        time=obj.timesheet.time_in
        return time
    
    def get_out_time(self,obj):
        time=obj.timesheet.time_out
        return time

    def get_date(self,obj):
        date=obj.timesheet.date
        return date

    def get_postion(self,obj):
        position=obj.postion.name
        return position
    def get_query_date(self,obj):
        date=obj.date
        return date
    
    def get_image(self,obj):
        request = self.context.get('request')
        try:
            appInfo_id=obj.timesheet.applicant.id
            obj=ApplicantDeatails.objects.get(user_id=appInfo_id)
            images=obj.image
            photo_url=images.url
            return request.build_absolute_uri(photo_url)
        except:
            return None

    def get_message(self,obj):
        msg=QueryMessage.objects.filter(query=obj)
        l=list()
        
        for i in msg:
            t=dict()
            
            try:
                t['msg']=i.message
                t['sender']=i.sender.id
                t['reciever']=i.reciver.id
                print(t)
            except:
                pass
            l.append(t)
    
        # s=json.dumps(l)
        return l
           
    def get_query_status(self,obj):
        status=obj.timesheet.resolve_status
        if status==False:
            return 0
        else:
            return 1
        

class GetMessageSerialize(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields='__all__'