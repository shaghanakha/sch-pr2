from django.contrib import admin
from .models import News, Exercise, Lesson, AnswerExercise
from guardian.admin import GuardedModelAdmin


class LessonAdmin(GuardedModelAdmin):
    pass


class NewsAdmin(GuardedModelAdmin):
    pass


class ExerciseAdmin(GuardedModelAdmin):
    pass


class AnswerExerciseAdmin(GuardedModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(AnswerExercise, AnswerExerciseAdmin)
