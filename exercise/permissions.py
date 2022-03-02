from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions
from django.contrib.auth.models import Group
from copy import deepcopy


class TeacherPermOnListViews(DjangoModelPermissions):

    def __init__(self):
        self.perms_map = deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.add_%(model_name)s', '%(app_label)s.view_%(model_name)s']


class TeacherPermOnDetailViews(DjangoModelPermissions):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user == obj.teacher or request.user.is_staff:
                return True
            elif obj.teacher in request.user.has_teacher()[0]:
                return True

        return bool(request.user == obj.teacher or request.user.is_staff)


#

class StudentPerm(DjangoModelPermissions):

    def has_permission(self, request, view):
        if request.user.has_teacher()[1]:
            return True
        elif request.user.is_staff:
            return True


class StudentEditPerm(DjangoModelPermissions):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user == obj.author or request.user == obj.exercise.teacher or request.user.is_staff:
                return True
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if request.user == obj.author and obj.access():
                return True
            if request.user == obj.exercise.teacher or request.user.is_staff:
                return True


class ProfilePerm(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user == obj or request.user.is_staff:
                return True
        if request.method in ("POST", "PUT", "PATCH"):
            if request.user == obj or request.user.is_staff:
                return True


class TeacherAddStudentPerm(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s']

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.teacher or request.user.is_staff)
