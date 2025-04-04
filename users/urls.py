from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
