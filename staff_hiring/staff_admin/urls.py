from django.contrib import admin
from django.urls import path, include
from .views import *
from staff_admin import views,view2
from encrypted_id import ekey

urlpatterns = [
    path("", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("myprofile/<int:id>", views.myprofile, name="myprofile"),
    path("change_password/", views.change_password, name="change_password"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path(
        "forgotpassword/forgotpasswordform/<slug>",
        views.forgot_password_form,
        name="forgot_password_form",
    ),
    path("employer/", views.employer_user_data, name="employer_user_data"),
    path("employer/view/<slug>", views.employer_view_data, name="employer_view_data"),
    path("applicant/", views.applicant_user_data, name="applicant_user_data"),
    path(
        "applicant/view/<slug>", views.applicant_view_data, name="applicant_view_data"
    ),
    path("emp_search/", views.emp_search, name="emp_search"),
    path("app_search/", views.app_search, name="app_search"),
    path("employer/add/", views.emp_add, name="emp_add"),
    path("employer/add/ajax/", views.emp_add_userdata, name="emp_add_userdata"),
    path("applicant/add/", views.app_add, name="app_add"),
    path("applicant/add/ajax/", views.app_add_userdata, name="app_add_userdata"),
    path(
        "employer_user_ajax/<int:id>",
        views.employer_user_ajax,
        name="employer_user_ajax",
    ),
    path(
        "applicant_user_ajax/<int:id>",
        views.applicant_user_ajax,
        name="applicant_user_ajax",
    ),
    path("employer/edit/<slug>", views.emp_edit_userdata, name="emp_edit_userdata"),
    path("applicant/edit/<slug>", views.app_edit_userdata, name="app_edit_userdata"),
    path("employer/del/<int:id>", views.emp_userdata_del, name="emp_userdata_del"),
    path("applicant/del/<int:id>", views.app_userdata_del, name="app_userdata_del"),
    path("logout/", views.logout, name="logout"),
    path("email/", views.Email_tem, name="Email_tem"),
    path("email/add/", views.add_email, name="add_email"),
    path("email/edit/<slug>", views.edit_email, name="edit_email"),
    path("email/del/<int:id>", views.del_email_tem, name="del_email_tem"),
    #     path('global/', views.global_setting, name='global_setting'),
    #     path('global/add/',
    #          views.add_global_setting, name='add_global_setting'),
    path("global/edit/<slug>", views.edit_global_setting, name="edit_global_setting"),
    #     path('global_setting/del/<slug>',
    #          views.del_global_setting, name='del_global_setting'),
    path("category/", views.category, name="category"),
    path("category/add/", views.add_category, name="add_category"),
    path("category/edit/<slug>", views.edit_category, name="edit_category"),
    path("category/del/<int:id>", views.del_category, name="del_category"),
    path("qr_code/", views.qr_code, name="qr_code"),
    path("del_qr/<int:id>", views.delete_qr, name="delete_qr"),
    path("chat/", views.chat_view, name="chat_view"),
    path("chat_ajax/", views.chat_ajax, name="chat_ajax"),
    path("reports/", views.reports_list, name="reports_list"),
    path("emp_pdf/", views.emp_pdf, name="emp_pdf"),
    path("app_pdf/", views.app_pdf, name="app_pdf"),
    path(
        "applicant_detail_list/<slug>",
        views.applicant_detail_list,
        name="applicant_detail_list",
    ),
    path("applicant_pdf/<slug>", views.applicant_data_pdf, name="applicant_data_pdf"),
    path(
        "applicant_user_data_pdf/<slug>",
        views.applicant_user_data_pdf,
        name="applicant_user_data_pdf",
    ),
    path(
        "employer/pdf/detail/list/<slug>",
        views.employer_detail_list,
        name="employer_detail_list",
    ),
    path("employer_pdf/<slug>", views.employer_data_pdf, name="employer_data_pdf"),
    path(
        "employer_user_data_pdf/<slug>",
        views.employer_user_data_pdf,
        name="employer_user_data_pdf",
    ),
    path("subadmin/", views.subadmin, name="subadmin"),
    path("subadmin/add/", views.add_subadmin, name="add_subadmin"),
    path("subadmin/edit/<slug>", views.edit_subadmin, name="edit_subadmin"),
    path("subadmin/del/<int:id>", views.del_submin, name="del_submin"),
    path("training/", views.training, name="training"),
    path("training/add/", views.add_training, name="add_training"),
    path("training/edit/<int:id>", views.edit_training, name="edit_training"),
    path("training/del_training/<int:id>", views.del_training, name="del_training"),
    path("emp_country_ajax/", views.emp_country_ajax, name="emp_country_ajax"),
    path(
        "emp_postal_code_ajax/", views.emp_postal_code_ajax, name="emp_postal_code_ajax"
    ),
    path("emp_state_city_ajax/", views.emp_state_city_ajax, name="emp_state_city_ajax"),
    path(
        "app_job_position_ajax/",
        views.app_job_position_ajax,
        name="app_job_position_ajax",
    ),
    path("contact/", views.contact, name="contact"),
    path("contact/reply/<int:id>", views.contact_reply, name="contact_reply"),
    path("contact/delete/<int:id>", views.del_contact, name="del_contact"),
    path("Cms_Pages/", views.Cms_Pages, name="Cms_Pages"),
    path("add_Cms_Pages/", views.add_Cms_Pages, name="add_Cms_Pages"),
    path("edit_Cms_Pages/<slug>", views.edit_Cms_Pages, name="edit_Cms_Pages"),
    path("delete_Cms_Pages/<slug>", views.delete_Cms_Pages, name="delete_Cms_Pages"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("aboutus/edit/<slug>", views.edit_aboutus, name="edit_aboutus"),
    path("team/", views.team, name="team"),
    path("team/add/", views.add_team, name="add_team"),
    path("team/edit/<slug>", views.edit_team, name="edit_team"),
    path("team/delete/<int:id>", views.del_team, name="del_team"),
    path("post/create/", views.post_create, name="post_create"),
    path("manage/shift/", views.manage_shift, name="manage_shift"),
    path("introduction/", views.App_intro, name="App_intro"),
    path("introduction/edit/<slug>", views.edit_App_intro, name="edit_App_intro"),
    path("socials/", views.social, name="social"),
    path("query/", views.query, name="query"),
    path("view/query/<int:id>", views.view_query, name="view_query"),
    path("delete_query/<int:id>", views.delete_query, name="delete_query"),
    path(
        "content/management/<slug>", views.content_management, name="content_management"
    ),
    path('liveChat/',view2.chatView),
    path('chatdetails/create/',view2.user_chat),
    

    # path('s_api/', views.s_api, name="s_api"),
    # path('s_api_details/<int:id>', views.s_api_details, name="s_api_details"),
]
