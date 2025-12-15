from rest_framework import generics, status
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util  # We need to create this for email sending

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            
            # Construct the absolute URL, but typically for SPA this should point to the frontend.
            # For now, we'll return the tokens or send an email link.
            # Assuming the user wants to test via API first or has a frontend route.
            # We'll construct a link that points to the API for verification, or a frontend URL.
            # Let's direct to a logical frontend URL structure.
            
            # absurl = 'http://'+current_site + relativeLink # This points to backend
            # Better to point to frontend. Let's assume frontend is on localhost:5173 for dev
            # or usage of an ENV variable for FRONTEND_URL.
            # For this task, getting the functionality working is key.
            # I will assume the email contains the RESET URL.
            
            # NOTE: Ideally we should use an env var for the frontend domain.
            # For now I will construct a generic link.
            
            absurl = f"http://localhost:5173/reset-password/{uidb64}/{token}"

            email_body = f'Hello, \n Use link below to reset your password  \n {absurl}'
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}

            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'success':True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
