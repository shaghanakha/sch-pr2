from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group


class TeacherPerm(BasePermission):
    def has_permission(self, request, view):
        if Group.objects.get(name="teacher_perm") in request.user.groups.all() or request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.teacher or request.user.is_staff)


class StudentPerm(BasePermission):

    def has_permission(self, request, view):
        if request.user.has_teacher()[1]:
            return True
        elif request.user.is_staff:
            return True


class ExercisePerm(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user == obj.teacher:
            return True


class StudentEditPerm(BasePermission):

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
