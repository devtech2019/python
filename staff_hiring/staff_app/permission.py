from asyncio.proactor_events import constants
import re
from rest_framework import permissions
from staff_admin.models import User
from rest_framework.response import Response


class IsAdmin(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # if obj.author == request.user:
        #     return True

        # if request.user.is_staff and request.method not in self.edit_methods:
        #     return True

        # return False



class IsAdmin(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True




class IsAdmin(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        usr=request.user
        a=usr.is_superuser
        return a


class IsCompany(permissions.BasePermission):
    message = 'User not belongs to  client profile.'

    def has_permission(self, request, view):
        if request.user.roll=='employer':
            return True
        else:
            return False



class IsJobSeeker(permissions.BasePermission):
    message = 'User not belongs to  applicant profile.'

    def has_permission(self, request, view):
        if request.user.roll=='applicant':
            return True
        else:
            return False




class CommonUser(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user.roll=='employer' or request.user.roll=='applicant':
            return True
        else:
            return False