from django.urls import path
from rest_framework.permissions import AllowAny

from .apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (UserCreateAPIView, UserDestroyAPIView, UserUpdateAPIView, UserRetrieveAPIView, PaymentsListApiView,
                    PaymentsCreateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("payments/", PaymentsListApiView.as_view(), name="payments-list"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="create-payments"),
]
