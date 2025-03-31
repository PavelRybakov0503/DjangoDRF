from rest_framework.routers import SimpleRouter
from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                             LessonUpdateAPIView, LessonDestroyAPIView)
from django.urls import path

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
]

urlpatterns += router.urls
