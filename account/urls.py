from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.views import ProfileViewSet
from account.views import UserViewSet, ProfileViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include
from account.views import VerifyEmailView

user_router = DefaultRouter()
user_router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('users/', include(user_router.urls)),
    path('profile/', ProfileViewSet.as_view(), name='profile'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
