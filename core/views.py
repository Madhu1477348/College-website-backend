# ==========================================
#  IMPORTS
# ==========================================
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import logging

# Import app-specific models and serializers
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination,Popup
from .pagination import ExaminationPagination
from .serializers import (
    StaffSerializer, 
    NotificationSerializer, 
    MaterialSerializer, 
    BranchSerializer, 
    SubjectSerializer, 
    SyllabusSerializer, 
    ExaminationSerializer,
    PopupSerializer
)
from accounts.utils import Util



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
logger = logging.getLogger(__name__)

class ContactAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        subject = f"New Contact Form Submission: {data.get('subject')}"
        message = (
            f"Name: {data.get('firstName')} {data.get('lastName')}\n"
            f"Email: {data.get('email')}\n"
            f"Subject: {data.get('subject')}\n\n"
            f"Message:\n{data.get('message')}"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["madhuoffficial12@gmail.com"],
                fail_silently=False,  # 🔥 FORCE ERROR
            )

            return Response(
                {"message": "Email sent successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error("CONTACT EMAIL FAILED", exc_info=True)

            return Response(
                {
                    "error": "Email sending failed",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
# Popup ViewSet

class PopupViewSet(viewsets.ModelViewSet):
    queryset = Popup.objects.all().order_by("-created_at")
    serializer_class = PopupSerializer

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]