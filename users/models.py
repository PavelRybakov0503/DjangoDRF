from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True, null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='payments'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Payments(models.Model):
    """
    Модель для хранения информации о платежах, произведенных пользователями за курсы или уроки.

    Атрибуты:
        CASH (str): Строковое представление оплаты наличными.
        TRANSFER_TO_AN_ACCOUNT (str): Строковое представление оплаты переводом на счет.
        METHOD_CHOICES (tuple): Набор возможных способов оплаты.
        user (User): Ссылка на пользователя, совершившего оплату.
        payment_date (date): Дата совершения платежа (заполняется автоматически).
        paid_course (Course): Ссылка на оплаченный курс (может быть пустым, если оплачен урок).
        paid_lesson (Lesson): Ссылка на оплаченный урок (может быть пустым, если оплачен курс).
        payment_amount (int): Сумма оплаты (в целых единицах).
        payment_method (str): Способ оплаты (наличные или перевод на счет).
        payment_url (str): Ссылка на платежную сессию или квитанцию (необязательна).
        session_id (str): Идентификатор платежной сессии (необязателен).
    """
    CASH = "Наличные"
    TRANSFER_TO_AN_ACCOUNT = "Перевод на счет"

    METHOD_CHOICES = ((CASH, "Наличные"), (TRANSFER_TO_AN_ACCOUNT, "Перевод на счет"))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Пользователь",
    )
    payment_date = models.DateField(
        auto_now=True,
        verbose_name="Дата оплаты",
        null=True,
        blank=True,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=50, verbose_name="Способ оплаты", choices=METHOD_CHOICES
    )
    payment_url = models.URLField(
        max_length=450, verbose_name="Ссылка на оплату", null=True, blank=True
    )
    session_id = models.CharField(
        max_length=255, verbose_name="ID сессии", blank=True, null=True
    )

    def __str__(self):
        """
            Возвращает строковое представление платежа для удобного отображения в административной панели.

            Returns:
                str: Строка, содержащая пользователя и оплачиваемый курс или урок.
            """
        return f"{self.user} - {self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
