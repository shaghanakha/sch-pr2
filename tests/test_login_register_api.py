from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from accounts.models import User


class AccountTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("t_register")
        self.login_url = reverse("login")
        self.user_data = {
            "username": "user1",
            "first_name": "fname",
            "last_name": "lname",
            "password": "randompass",
            "national_code": "4343434343",
            "school_name": "schoolname",
            "lesson_name": "lessonname",
        }
        group = Group(name="teacher_perm")
        group.save()
        group2 = Group(name="student_perm")
        group2.save()
        self.client.post(self.register_url, self.user_data)
        self.account1 = User.objects.get(username="user1")

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_with_duplicate_data(self):
        self.client.post(self.register_url, self.user_data)
        res = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_login(self):
        res = self.client.post(self.login_url,
                               data={"username": self.user_data["username"], "password": self.user_data["password"]})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_edit_profile(self):
        self.client.force_login(user=self.account1)
        res = self.client.patch(
            reverse('profile', kwargs={'username': 'user1'}),
            data={"first_name": "changed"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='user1')
        self.assertEqual(user.first_name, "changed")
