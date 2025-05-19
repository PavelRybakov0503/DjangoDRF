import re
from rest_framework import serializers


class UrlValidator:
    """
    Валидатор для проверки, что поле содержит корректный URL-адрес YouTube.
    Запрещает размещение ссылок на сторонние образовательные платформы или личные сайты.
    """

    def __init__(self, field):
        """
        Конструктор валидатора.

        Аргументы
        - field (str): Название поля, которое необходимо валидировать.
        """
        self.field = field

    def __call__(self, value):
        """
        Проверяет, что значение поля соответствует формату URL YouTube.

        Аргументы
        - value (dict): Словарь со значениями полей.

        Исключения
        - serializers.ValidationError: Если значение не является URL YouTube.
        """
        # Компилируем регулярное выражение для поиска URL YouTube
        reg = re.compile("^(https?://)?(www.)?youtube.com/.+$")
        # Получаем значение поля для проверки
        tmp_val = dict(value).get(self.field)
        # Если значение не соответствует шаблону — выбрасываем ошибку
        if not bool(reg.match(tmp_val)):
            raise serializers.ValidationError(
                "Неверный URL-адрес. Пожалуйста, укажите правильный URL-адрес YouTube."
                "Нельзя размещать ссылки на сторонние образовательные платформы или личные сайты"
            )
