from django.urls import path
from exercise.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('teacher/news/', NewsListCreate.as_view(), name='news_list_create'),
                  path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
                  path('news/', NewsList.as_view(), name='news_list'),
                  path('teacher/addstudent/<int:pk>', LessonDetail.as_view(), name='lessons_detail'),
                  path('teacher/exercises/', ExerciseListCreate.as_view(), name='exercise_list_create'),
                  path('exercises/', ExerciseList.as_view(), name='exercise_list'),
                  path('exercises/<int:pk>', ExercisesDetail.as_view(), name='exercises_detail'),
                  path('exercises/answer/<int:e_id>', AnswerToExercise.as_view(), name='answer_add'),
                  path('answer/<int:pk>', AnswerExerciseDetail.as_view(), name='answer_detail'),
                  path('answer/', Answers.as_view(), name='answers_list'),
                  path('teacher/answer/', CheckAnswers.as_view(), name='t_answers_list'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
