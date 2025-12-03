from django.contrib import admin
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination
# Register your models here.
admin.site.register(Staff)
admin.site.register(Notification)
admin.site.register(Material)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Syllabus)
admin.site.register(Examination)

