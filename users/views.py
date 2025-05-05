from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .models import Payment, User, Payments
from .serializers import PaymentSerializer, UserProfileSerializer
from .filters import PaymentFilter
from rest_framework.generics import CreateAPIView
from users.serializers import UserSerializer
from .services import create_product_in_stripe, create_price_in_stripe, create_session_in_stripe


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['date']  # Сортировка по умолчанию


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsListApiView(generics.ListAPIView):
    """
       Представление для получения списка всех платежей.

       Позволяет:
           - Получать все записи платежей;
           - Фильтровать по курсу, уроку или способу оплаты;
           - Сортировать по дате оплаты.

       Атрибуты:
           serializer_class (PaymentsSerializer): Сериализатор для вывода платежей;
           queryset (QuerySet): Все объекты модели Payments;
           filter_backends (list): Список фильтров для поиска и сортировки;
           filterset_fields (tuple): Поля, по которым можно фильтровать;
           ordering_fields (tuple): Поля, по которым можно сортировать.
       """
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class PaymentsCreateAPIView(generics.CreateAPIView):
    """
        Представление для создания нового платежа.

        Позволяет:
            - Создать новую запись о платеже;
            - Привязывает пользователя к платежу автоматически;
            - Интегрируется с платежной системой Stripe (создание продукта, цены и платежной сессии).

        Атрибуты:
            serializer_class (PaymentsSerializer): Сериализатор для создания платежа;
            queryset (QuerySet): Все объекты модели Payments.
        """
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        """
            Дополнительная логика при создании платежа.

            Действия:
                1. Сохраняет платеж с помощью сериализатора, связывает с текущим пользователем.
                2. Создаёт продукт в Stripe по данным платежа.
                3. Создаёт цену для этого продукта в Stripe.
                4. Запускает платёжную сессию в Stripe, получает ID сессии и ссылку на оплату.
                5. Сохраняет session_id и payment_url в объекте платежа.

            Аргументы:
                serializer (PaymentsSerializer): Сериализатор для сохранения данных платежа.
            """
        payment = serializer.save()
        payment.user = self.request.user
        stripe_product_id = create_product_in_stripe(payment)
        price = create_price_in_stripe(stripe_product_id, payment.payment_amount)
        session_id, payment_link = create_session_in_stripe(price)
        payment.session_id = session_id
        payment.payment_url = payment_link
        payment.save()
