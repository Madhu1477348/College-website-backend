from rest_framework import viewsets
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination
from .serializers import StaffSerializer, NotificationSerializer, MaterialSerializer, BranchSerializer, SubjectSerializer, SyllabusSerializer, ExaminationSerializer

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
    queryset = Examination.objects.all().order_by('-date')
    serializer_class = ExaminationSerializer


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









