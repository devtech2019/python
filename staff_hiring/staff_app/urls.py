from django.contrib import admin
from django.urls import path, include
from staff_app import views,view2


urlpatterns = [
    path('getCountry/',views.countryView),
    path('getCity/',views.cityView),
    path('getState/',views.stateView),
    path('appIntro/',views.appIntro),
    path('user_register',views.registerEmp),
    path('enquiry',views.enquiry),
    path('yearlist',views.yearList),
    path('newPasswordReset',views.newPasswordSet),
    path('vaccinatelist',views.vaccinaList),
    path('getuserdetails/',views.getUserDetails),
    path('gettraining/',views.getTraining),
    
    path('login/email',views.CustomAuthToken.as_view()),
    path('login/email/mail_confirm/<int:a>/',views.mailConfirm),
    path('user_register/mail_confirm/<int:a>',views.mailConfirm),
    path('otp_verification/login',views.OTP_Verification),
    path('login/mobile',views.mobile_login),
    path('contact_confirm/',views.contact_noConfirm),
    path('job_category/',views.category),
    path('shift_post_create',views.postShift),
    # path('shift',views.accepted_shift),
    # path('pending_shift',views.pending_shift),
    path('shift_post_list/',views.shitfPostList),
    path('shift_post_delete',views.shitfPostDelete),
    path('shift_cancel',views.shitfPostCancel),
    path('timeSheetSubmitList',views.submitTimeSheetList),
    path('timeSheetApprove',views.timeSheetApprove),
    path('timeSheetQuery',views.timeSheetQuery),
    path('getTimeSheetdetails/',views.ApproveTimeSheetDetails),
    path('getquerydetails/',views.getQuery),
    path('sendquery',views.sendQuery),
    path('queryResolve/',views.queryResolve),
    path('getbosterdose/',views.getBooster),
    path('getRoomId/',views.getRoomId),
    path('getMessage/',views.getMessage),
    
    
   
    path('User_profile_update',views.UserProfileUpdate),
   
   
    path('compnay_info_create',views.employeeDetails),
    path('client_feedback',views.feedback_emp),


    #applicantapp-------view
    path('applicant_info_create',view2.applicantDetails),
    path('shift_booking',view2.shiftBooking),
    #path('applicant_profile_update',view2.applicantProfileUpdate),
    path('shift_details/',view2.shift_details),
    path('shift_listing',view2.shiftListByStatus),
    # path('applicant_booked/',view2.booked_shift),
    #path('applicant_register',view2.registerApplicant),
    # path('available_shift',view2.available_shift),
    path('test',views.testview),
    path('timesheet/',view2.timeSheet),
    path('submitTimeSheet',view2.submitTimeSheet),
    path('timeSheetSatatus',view2.timeSheetStatus),
    path('shift_like',view2.likeShift),
    path('fovrite_post',view2.favoriteList),
    path('shift_booking_cancel',view2.shiftBookingCancel),
    path('userDueTimeSheetPostList',view2.postListForTimeSheet),


    #common view
    
    path('set_notification',views.set_notifcation),
    path('change_password',views.changePassword),
    path('forget_password',views.forgetPassword),
    path('forgetpass/otp_verify',views.OTP_verified),
    path('aboutUs/', views.aboutUs),
    path('cms/',views.cms_page),
    #path('privacy_policy',views.privacy_policy),

    path('32test/',views.app_pdf),

    
]
