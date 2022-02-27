from abc import ABC

from rest_framework import serializers

from .models import Lesson, Exercise, News, AnswerExercise

global ExerciseSerializer


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    teacher = serializers.StringRelatedField()
    class_title = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()
    date = serializers.DateTimeField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='exercises_detail')

    class Meta:
        model = Exercise
        fields = (
            "url",
            "lesson",
            "teacher",
            "class_title",
            "title",
            "file",
            "body",
            "date",
            "deadline",
        )

    def create(self, validated_data):
        exe = Exercise.objects.create(**validated_data)
        lesson = Lesson.objects.get(teacher=validated_data["teacher"])
        exe.lesson = lesson
        exe.save()
        return exe


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    teacher = serializers.StringRelatedField()
    students = serializers.StringRelatedField(read_only=True, many=True)
    add_student_national_code = serializers.CharField(write_only=True)

    class Meta:
        model = Lesson
        fields = (
            "title",
            "add_student_national_code",
            "teacher",
            "students",
        )

    def update(self, instance, validated_data):
        student_nationalcode = validated_data.get(
            'add_student_national_code'
        )
        instance.add_student(national_code=student_nationalcode)
        return instance


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    teacher = serializers.StringRelatedField()
    date = serializers.DateTimeField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='news_detail')

    class Meta:
        model = News
        fields = (
            "url",
            "teacher",
            "title",
            "body",
            "date",
        )


class AnswerExerciseSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    exercise = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name='answer_detail')
    file = serializers.FileField()
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnswerExercise
        fields = (
            "url",
            "exercise",
            "body",
            "file",
            "date",
            "author",
        )


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    exercise = serializers.StringRelatedField()
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnswerExercise
        fields = (
            "exercise",
            "body",
            "file",
            "date",
            "author",
        )
