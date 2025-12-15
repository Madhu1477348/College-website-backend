# ==========================================
#  IMPORTS
# ==========================================
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

# Import app-specific models and serializers
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination
from .pagination import ExaminationPagination
from .serializers import (
    StaffSerializer, 
    NotificationSerializer, 
    MaterialSerializer, 
    BranchSerializer, 
    SubjectSerializer, 
    SyllabusSerializer, 
    ExaminationSerializer
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