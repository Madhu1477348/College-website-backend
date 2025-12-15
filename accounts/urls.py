from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserDetailView, CustomTokenObtainPairView, 
    RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView, 
    UserViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # API Router URLs
    path('', include(router.urls)),

    # Auth URLs
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('me/', UserDetailView.as_view(), name='auth_me'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password Reset URLs
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]