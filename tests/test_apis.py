from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from exercise.models import Lesson, News
from exercise.models import User
from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm
from model_mommy import mommy
from django.conf import settings


class ViewsTest(APITestCase):
    def setUp(self):
        self.account1 = mommy.make(User, school_name="schoolname", lesson_name="lessonname")
        self.account2 = mommy.make(User, school_name="schoolname", lesson_name="lessonname")
        self.l1 = mommy.make(Lesson, teacher=self.account1)
        self.l2 = mommy.make(Lesson, teacher=self.account2)
        self.l2 = mommy.make(News, teacher=self.account2)
        mommy.make(Group, name="student_perm")
        mommy.make(Group, name="teacher_perm")
        self.sample_news = mommy.make(News, teacher=self.account1)

    def test_teacher_can_add_student(self):
        assign_perm("exercise.change_lesson", self.account1)
        self.client.force_login(user=self.account1)
        res = self.client.put(
            reverse('lessons_detail', kwargs={'pk': self.l1.id}),
            data={"add_student_national_code": "1111111111"}, format='json')
        student = User.objects.get(username="1111111111")
        lesson = Lesson.objects.get(id=self.l1.id)
        students = lesson.students.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(student in students)

    def test_teacher_cannot_add_student_in_others_lesson(self):
        assign_perm("exercise.change_lesson", self.account1)
        self.client.force_login(user=self.account1)
        res = self.client.get(
            reverse('lessons_detail', kwargs={'pk': self.l2.id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_news(self):
        assign_perm("exercise.add_news", self.account1)
        self.client.force_login(user=self.account1)
        res = self.client.post(
            reverse('news_list_create'),
            data={"title": "t1", "body": "b1"}, format='json')
        news = News.objects.filter(title="t1")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(news)

    def test_edit_news(self):
        assign_perm("exercise.change_news", self.account1)
        assign_perm("exercise.view_news", self.account1)
        self.client.force_login(user=self.account1)
        res = self.client.patch(
            reverse('news_detail', kwargs={'pk': self.sample_news.id}),
            data={"title": "changed"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news = News.objects.get(id=self.sample_news.id)
        self.assertEqual(news.title, "changed")
