from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.urls import reverse
from .permissions import *


class NewsListCreate(generics.ListCreateAPIView):
    """for teachers to add or view their news"""
    permission_classes = (IsAuthenticated, DjangoModelPermissions, TeacherPerm)
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return News.objects.all()
        else:
            query = News.objects.filter(teacher=user)
            return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class NewsList(generics.ListAPIView):
    """for students to view their teachers news"""
    permission_classes = (IsAuthenticated, DjangoModelPermissions, StudentPerm)
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        a = user.has_teacher()
        if a[1]:
            query = News.objects.filter(teacher__in=a[0])
            return query


class ExerciseListCreate(generics.ListCreateAPIView):
    """for teachers to add or view their exercises"""
    permission_classes = (IsAuthenticated, DjangoModelPermissions, TeacherPerm)
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Exercise.objects.all()
        else:
            query = Exercise.objects.filter(teacher=user)
            return query

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class ExerciseList(generics.ListAPIView):
    """for students to view their exercises"""
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        a = user.has_teacher()
        if a[1]:
            query = Exercise.objects.filter(teacher__in=a[0])
            return query


class Answers(generics.ListAPIView):
    """for students to view their answer"""
    permission_classes = (IsAuthenticated, StudentPerm, DjangoModelPermissions)
    serializer_class = AnswerExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AnswerExercise.objects.all()
        else:
            return AnswerExercise.objects.filter(author=user)


class CheckAnswers(generics.ListAPIView):
    """for teachers to view their students answers"""
    permission_classes = (IsAuthenticated, DjangoModelPermissions, TeacherPerm)
    serializer_class = AnswerExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AnswerExercise.objects.all()
        else:
            return AnswerExercise.objects.filter(exercise__teacher=user)


class AnswerToExercise(APIView):
    """for students to answer to their exercises"""
    permission_classes = (IsAuthenticated, StudentPerm)
    serializer_class = AnswerExerciseSerializer

    def get(self, request, e_id):
        if AnswerExercise.objects.filter(exercise__id=e_id, author=request.user).exists():
            return HttpResponseRedirect(reverse('answers_list'))
        else:
            exe = get_object_or_404(Exercise, id=e_id)
            return Response({"answer to": str(exe)})

    def post(self, request, e_id):
        answer_serializer = AnswerSerializer(data=request.data)
        if answer_serializer.is_valid():
            exe = get_object_or_404(Exercise, id=e_id)
            if AnswerExercise.objects.filter(exercise=exe, author=request.user):
                return Response({'message': 'you already answered'})
            if timezone.now() > exe.deadline:
                return Response({'message': 'Deadline is expired!'})
            if exe.teacher not in request.user.has_teacher()[0]:
                return Response({'message': 'you are not in teacher list!'})
            Answer = AnswerExercise.objects.create(exercise=exe, author=request.user)
            Answer.body = answer_serializer.data['body']
            Answer.file = answer_serializer.data['file']
            Answer.save()
            return Response({'message': 'Done!'})
        return Response({'message': answer_serializer.errors})


class ExercisesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ExercisePerm, DjangoModelPermissions)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class AnswerExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, StudentEditPerm, DjangoModelPermissions)
    queryset = AnswerExercise.objects.all()
    serializer_class = AnswerExerciseSerializer


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, TeacherPerm, DjangoModelPermissions)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, TeacherPerm, DjangoModelPermissions)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
