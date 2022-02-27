from rest_framework import serializers

from .models import User
from exercise.models import Lesson
from django.contrib.auth.models import Group


class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "password", "national_code", "school_name", "lesson_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.groups.add(Group.objects.get(name="teacher_perm"))
        user.save()
        lesson = Lesson.objects.create(title=user.lesson_name, teacher=user)
        lesson.save()
        return user

    def validated_national_code(self, value):
        if value.isnumeric() and len(value) == 10:
            return True
        else:
            raise serializers.ValidationError('national code not valid!')


class UpdateProfile(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "password", "national_code")
        read_only_fields = ("national_code",)

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username
        )
        instance.set_password(validated_data.get(
            'password', instance.password
        ))
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )

        instance.save()
        return instance
