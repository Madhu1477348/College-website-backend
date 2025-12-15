from django.contrib import admin
from .models import Staff, Notification, Material, Branch, Subject, Syllabus, Examination, Popup
# Register your models here.
admin.site.register(Staff)
admin.site.register(Notification)
admin.site.register(Material)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Syllabus)
admin.site.register(Popup)
@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "exam_type", "date")
    list_filter = ("category", "exam_type")
    search_fields = ("title",)

