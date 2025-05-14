from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'course')
