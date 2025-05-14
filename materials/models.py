from django.conf import settings
from django.db import models


class Course(models.Model):
    """
       Модель курса.

       Атрибуты
       - title: Название курса (до 100 символов).
       - preview: Превью-изображение курса (опционально).
       - description: Описание курса (опционально).
       - owner: Владелец курса (пользователь, опционально).

       Методы
       - __str__: Возвращает название курса.
       """
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/courses/preview", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """
        Модель урока.

        Атрибуты
        - title: Название урока (до 100 символов).
        - description: Описание урока (опционально).
        - preview: Превью-изображение урока (опционально).
        - video_url: Ссылка на видео (опционально).
        - course: Курс, к которому относится урок.
        - owner: Владелец урока (пользователь, опционально).

        Методы
        - __str__: Возвращает название урока.
        """
    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        upload_to="materials/lessons/preview", blank=True, null=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """
        Модель подписки на курс.

        Атрибуты
        - user: Пользователь, оформивший подписку.
        - course: Подписанный курс.
        - created_at: Дата и время оформления подписки.
        - is_active: Признак активности подписки.

        Методы
        - __str__: Показывает связь пользователя и курса.

        Meta
        - unique_together: Ограничение уникальности по комбинации пользователь+курс.
        """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} -> {self.course}"
