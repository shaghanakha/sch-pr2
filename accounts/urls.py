from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import TeacherRegistration, LogoutAPIView, Profile

urlpatterns = [
    path('login/', obtain_auth_token, name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('register/teacher/', TeacherRegistration.as_view(), name="t_register"),
    path('profile/<str:username>', Profile.as_view(), name="profile"),
]
