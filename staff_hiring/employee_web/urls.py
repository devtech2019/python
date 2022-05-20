from django.contrib import admin
from django.urls import path, include
from .views import *
from employee_web import views, view2

urlpatterns = [
    path("", views.home, name="home"),
    path("contact-us/", views.Contact, name="Contact"),
    path("login/", views.login, name="emp_login"),
    path("login/otp/<slug>", views.login_otp, name="login_otp"),
    path("profile/<slug>", views.user_profile, name="user_profile"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("verifyotp/<slug>", views.verify_otp, name="verify_otp"),
    path("resendotp/<slug>", views.resend_otp, name="resend_otp"),
    path("manage/shift/", view2.manage_shift, name="manage_shift"),
    path(
        "manage/shift/sorting/", view2.sorting_manage_shift, name="sorting_manage_shift"
    ),
    path(
        "manage/shift/search/",
        view2.search_sorting_manage_shift,
        name="search_sorting_manage_shift",
    ),
    #     path('time/sheet/', views.time_sheet, name='time_sheet'),
    path("notifications/", views.notifications, name="notifications"),
    path(
        "notifications/setting",
        views.notifications_setting,
        name="notifications_setting",
    ),
    path("notifications/help", views.no_notifications, name="no_notifications"),
    path("passwordresetform/<slug>", views.passwordresetform, name="passwordresetform"),
    path("client/sign-up/", views.emp_sign_up, name="emp_sign_up"),
    path("client/otp-verify/<slug>", views.emp_otp_verify, name="emp_otp_verify"),
    path("client/resend-otp/<slug>", views.emp_resend_otp, name="emp_resend_otp"),
    path("client/change-password", views.Change_password, name="Change_password"),
    path("applicant/otp-verify/<slug>", views.app_otp_verify, name="app_otp_verify"),
    path("applicant/resend-otp/<slug>", views.app_resend_otp, name="app_resend_otp"),
    path(
        "client/company-profile/<user_slug>",
        views.update_company_profile,
        name="update_company_profile",
    ),
    path(
        "profile/company-profile/<slug>",
        views.emp_company_information,
        name="emp_company_information",
    ),
    path("otp_verify_ajax/<slug>", views.otp_verify_ajax, name="otp_verify_ajax"),
    path("applicant/sign-up/", views.app_sign_up, name="app_sign_up"),
    path(
        "applicant/vaccination/<slug>",
        views.app_vaccation_information,
        name="app_vaccation_information",
    ),
    path("logout/", views.logout, name="emp_logout"),
    path("about", views.about_us, name="about_us"),
    path("emp_country_ajax/", views.emp_country_ajax, name="emp_country_ajax"),
    path("emp_lat_lng/", views.emp_data_ajax, name="emp_data_ajax"),
    path("app_lat_lng/", views.app_data_ajax, name="app_data_ajax"),
    path(
        "emp_postal_code_ajax/", views.emp_postal_code_ajax, name="emp_postal_code_ajax"
    ),
    path("emp_state_city_ajax/", views.emp_state_city_ajax, name="emp_state_city_ajax"),
    # view2 file url
    path("shift_post_create/", view2.shiftPostCreate, name="shiftPostCreate"),
    path("del_post/<int:id>", view2.delete_post, name="delete_post"),
    path("time_sheet_manage/", view2.time_sheet, name="time_sheet"),
    path("manage_shift/", view2.manage_shift, name="manage_shift"),
    path("querySubmit/<int:a>/", view2.queryView, name="querySubmit"),
    path("approveFormSubmit/<int:a>/", view2.approvedView, name="approveFormSubmit"),
    path("timesheet/details/", view2.timeSheetDetails, name="timesheetdetails"),
    path("term-and-condition/", view2.termcondition, name="termcondition"),
    path("timesheet_filter/", view2.timeSheetFilter, name="timesheetfilter"),
    path(
        "admin_reply_in_view_query/<int:id>",
        view2.admin_reply_in_view_query,
        name="admin_reply_in_view_query",
    ),
    path("emp_reply/", view2.emp_reply, name="emp_reply"),
    path("resolve_status/", view2.resolve_status, name="resolve_status"),
    path("f/", view2.f, name="f"),
    path("chats/", view2.chats, name="chats"),
    path('help_chat/',view2.helpChatView),
]
