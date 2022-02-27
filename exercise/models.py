from django.db import models
from django.utils import timezone
from accounts.models import User
from django.contrib.auth.models import Group


class Lesson(models.Model):
    title = models.CharField(max_length=60)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    students = models.ManyToManyField(User, blank=True, related_name='student')
    add_student_national_code = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def add_student(self, national_code):
        try:
            student = User.objects.get(national_code=national_code)
            return self.students.add(student)
        except models.ObjectDoesNotExist:
            student = User.objects.create(national_code=national_code, username=str(national_code))
            student.set_password(str(national_code))
            student_perm_group = Group.objects.get(name='student_perm')
            student.groups.add(student_perm_group)

            student.save()
            return self.students.add(student)

    def __str__(self):
        return f"{self.title}"


class News(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=60)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.teacher}"


class Exercise(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=60)
    body = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='pdf/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.title} by {self.teacher}"


class AnswerExercise(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def access(self):
        if timezone.now() > self.exercise.deadline:
            return False
        else:
            return True
