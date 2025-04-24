from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    """
        Сериализатор для модели Lesson.

        Используется для преобразования объектов уроков в формат JSON и обратно.

        Валидаторы
        - UrlValidator: Проверяет валидность ссылки на видео в поле "video_url".
        """
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_url")]


class SubscriptionSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Subscription.

        Используется для преобразования объектов подписок пользователя на курсы.
        """
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """
        Сериализатор для модели Course.

        Добавляет к стандартным полям курса дополнительные вычисляемые поля:
        - lesson_count: Количество уроков в курсе.
        - lessons: Список сериализованных уроков, входящих в курс.
        - is_subscribed: Признак того, подписан ли текущий пользователь на курс.

        Методы
        - get_lesson_count: Получает количество уроков для курса.
        - get_is_subscribed: Проверяет активную подписку пользователя на курс.
        """
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    # def get_lessons_count(self, instance):
    #     return instance.lessons.all().count()
    #
    # def get_subscription(self, instance):
    #     user = self.context["request"].user
    #     return Subscription.objects.filter(user=user).filter(course=instance).exists()

    def get_lesson_count(self, obj):
        """
                Возвращает количество уроков, связанных с данным курсом.

                Аргументы
                - obj: Экземпляр курса.

                Результат
                - int: Количество уроков.
                """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
                Проверяет, подписан ли текущий пользователь на курс.

                Аргументы
                - obj: Экземпляр курса.

                Результат
                - bool: True, если подписка оформлена, иначе False.
                """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(course=obj, user=request.user).exists()
        return False
