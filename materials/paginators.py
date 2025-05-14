from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
        Кастомная пагинация для отображения списка объектов с поддержкой изменения размера страницы по запросу
         пользователя.

        Атрибуты
        - page_size: Количество объектов на одной странице по умолчанию (10).
        - page_size_query_param: Имя GET-параметра, позволяющего клиенту изменять размер страницы ("page_size").
        - max_page_size: Максимально допустимое количество объектов на странице (100).
        """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
