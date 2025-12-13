from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .pagination import ExaminationPagination
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination
from .serializers import StaffSerializer, NotificationSerializer, MaterialSerializer, BranchSerializer, SubjectSerializer, SyllabusSerializer, ExaminationSerializer

class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SyllabusViewSet(ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer

class ExaminationViewSet(ModelViewSet):
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

class ContactAPIView(APIView):
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









