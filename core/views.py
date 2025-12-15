# ==========================================
#  IMPORTS
# ==========================================
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

# Import app-specific models and serializers
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination
from .pagination import ExaminationPagination
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
    UserManagementSerializer,
    StaffSerializer, 
    NotificationSerializer, 
    MaterialSerializer, 
    BranchSerializer, 
    SubjectSerializer, 
    SyllabusSerializer, 
    ExaminationSerializer
)
from .utils import Util

# ==========================================
#  AUTH VIEWS
# ==========================================
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

# ==========================================
#  USER MANAGEMENT (For Admin Dashboard)
# ==========================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserManagementSerializer
    permission_classes = [IsAdminUser]

# ==========================================
#  APP CONTENT VIEWSETS
# ==========================================
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer

class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all().order_by("-date")
    serializer_class = ExaminationSerializer
    permission_classes = [AllowAny]
    pagination_class = ExaminationPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        exam_type = self.request.query_params.get("exam_type")

        if category:
            queryset = queryset.filter(category=category)

        if exam_type:
            queryset = queryset.filter(exam_type=exam_type)

        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

# ==========================================
#  CONTACT API
# ==========================================
class ContactAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            subject = f"New Contact Form Submission: {data.get('subject')}"
            message = f"""
            Name: {data.get('firstName')} {data.get('lastName')}
            Email: {data.get('email')}
            Subject: {data.get('subject')}
            
            Message:
            {data.get('message')}
            """
            
            # Using your existing send_email Utility if it works, or fallback to django send_mail
            email_data = {
                'email_body': message,
                'to_email': 'madhuoffficial12@gmail.com',  # Your desired recipient email
                'email_subject': subject
            }
            try:
                # Try using the Util class first
                Util.send_email(email_data)
            except:
                # Fallback to Django send_mail if Util fails or is missing config
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@college.edu',
                    ['madhuoffficial12@gmail.com'],
                    fail_silently=False,
                )

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)