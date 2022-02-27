from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    national_code = models.DecimalField(max_digits=10, decimal_places=0, unique=True, null=True, blank=True)
    school_name = models.CharField(max_length=30, blank=True, null=True)
    lesson_name = models.CharField(max_length=30, blank=True, null=True)

    def has_teacher(self):
        from exercise.models import Lesson

        teachers = list()
        for obj in Lesson.objects.all():
            if self in obj.students.all():
                teachers.append(obj.teacher)
        if len(teachers) != 0:
            return teachers, True
        else:
            return teachers, False
