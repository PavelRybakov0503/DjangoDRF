from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerators, IsOwner
from django.utils import timezone
from datetime import timedelta
from .tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    """
        ViewSet для работы с курсами.

        Реализует стандартные CRUD-операции (создание, получение, изменение, удаление).
        Использует пагинацию и настраиваемые permissions для разных типов запросов.

        Методы
        - get_permissions: Определяет права доступа для текущего действия (action).
        """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """
                Определяет права доступа для разных действий:
                - create: модераторам запрещено создавать
                - update, retrieve: разрешено модераторам или владельцу
                - destroy: разрешено только владельцу
                """
        if self.action == "create":
            self.permission_classes = (~IsModerators,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerators | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                # ~IsModerators,
                IsOwner,
            )
        return super().get_permissions()

    def update_course(request, course_id):
        course = get_object_or_404(Course, id=course_id)
        now = timezone.now()

        # Проверка времени последнего обновления (например, поле course.last_updated)
        if course.last_updated and (now - course.last_updated) < timedelta(hours=4):
            # Только сохраняем изменения, рассылку не делаем
            course.save()
            return JsonResponse({'status': 'updated without notification'})

        # Обновление курса
        course.last_updated = now
        course.save()

        # Получение подписчиков курса
        subscribers = course.subscriptions.all()
        for subscriber in subscribers:
            send_course_update_email.delay(subscriber.user.email, course.title, "курс")

        return JsonResponse({'status': 'update and notification sent'})

    # def get_permissions(self):
    #     if self.action in ['destroy', 'create']:
    #         #  Запретить модераторам удалять и создавать
    #         self.permission_classes = [IsAuthenticated]
    #     elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
    #         # Разрешить модераторам и прошедшим проверку подлинности пользователям просматривать и редактировать
    #         self.permission_classes = [IsAuthenticated, IsModerators]
    #     return [permission() for permission in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    """
        ViewSet для работы с уроками.

        Реализует стандартные CRUD-операции с уроками курса.
        Разграничивает права доступа на действия.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
                Определяет права доступа для разных операций над уроками, например:
                - create, destroy: только для аутентифицированного пользователя
                - list, retrieve, update, partial_update: для аутентифицированных пользователей и модераторов
                """
        if self.action in ['destroy', 'create']:
            # Запретить модераторам удалять и создавать
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            # Разрешить модераторам и прошедшим проверку подлинности пользователям просматривать и редактировать
            self.permission_classes = [IsAuthenticated, IsModerators]
        return [permission() for permission in self.permission_classes]

    def update_lesson(request, course_id, lesson_id):
        course = get_object_or_404(Course, id=course_id)
        now = timezone.now()

        # Проверка на отправку уведомления (раз в 4 часа для курса)
        if course.last_updated and (now - course.last_updated) < timedelta(hours=4):
            # Только сохранить обновление урока
            lesson = get_object_or_404(Lesson, id=lesson_id)
            lesson.save()
            return JsonResponse({'status': 'lesson updated, no notification'})

        # Обновить урок и курс, рассылка
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.save()
        course.last_updated = now
        course.save()

        subscribers = course.subscriptions.all()
        for subscriber in subscribers:
            send_course_update_email.delay(subscriber.user.email, course.title, f"урок {lesson.title}")

        return JsonResponse({'status': 'lesson updated, notification sent'})


class LessonCreateAPIView(generics.CreateAPIView):
    """
        Представление для создания нового урока.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """
        Представление для просмотра списка всех уроков с поддержкой пагинации.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
        Представление для просмотра одного конкретного урока.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
       Представление для обновления данных урока.
       """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
        Представление для удаления урока.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class ToggleSubscriptionAPIView(APIView):
    """
        Представление для подписки/отписки пользователя от курса.

        POST-запрос с course_id:
        - Если подписка уже существует, она удаляется.
        - Если подписки нет, она создается.

        Возвращает сообщение об успешном действии.
        """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
                Обрабатывает подписку/отписку пользователя на курс по course_id.
                """
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
        Представление для создания новой подписки на курс для пользователя.
        """
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        """
                Создание подписки, если она ещё не оформлена.
                Если подписка уже есть, можно реализовать возврат соответствующего сообщения.
                """
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item, is_active=True)
            message = "Подписка добавлена"

        return Response({"message": message})
