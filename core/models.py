from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    category_of_post = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='staff_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    CATEGORY_CHOICES = (
        ('inter', 'Inter'),
        ('degree', 'Degree'),
        ('general', 'General'),
    )
    NOTIFICATION_TYPES = (
        ('general', 'General'),
        ('exam', 'Examination'),
        ('admission', 'Admission'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    file = models.FileField(upload_to='notifications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    CATEGORY_CHOICES = (
        ('inter', 'Inter'),
        ('degree', 'Degree'),
    )
    YEAR_CHOICES = (
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
    )
    subject = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='inter')
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    file = models.FileField(upload_to='materials/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.year}"

class Branch(models.Model):
    COURSE_TYPE_CHOICES = (
        ('inter', 'Inter'),
        ('degree', 'Degree'),
    )

    BRANCH_CHOICES = (
        # Inter Branches
        ('MPC', 'M.P.C'),
        ('BiPC', 'Bi.P.C'),
        ('CEC', 'C.E.C'),
        ('MEC', 'M.E.C'),
        ('MBiPC', 'M.Bi.P.C'),
        
        # Degree Branches
        ('BSc', 'B.Sc'),
        ('MPCs', 'M.P.Cs'),
        ('BCom', 'B.Com'),
        ('BZC', 'B.Z.C'),
    )

    name = models.CharField(max_length=100, choices=BRANCH_CHOICES)  
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.get_course_type_display()})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')
    year = models.CharField(max_length=20, blank=True, null=True)  # e.g., "1st Year", "2nd Year"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.branch.name}"

class Syllabus(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='syllabi')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='syllabus/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # For external links
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Syllabi"

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

class Examination(models.Model):
    CATEGORY_CHOICES = (
        ('inter', 'Inter'),
        ('degree', 'Degree'),
    )

    EXAM_TYPE_CHOICES = (
        ('unit', 'Unit Test'),
        ('half', 'Half-Yearly'),
        ('pre', 'Pre-Final'),
        ('mid', 'Mid Exam'),
        ('semester', 'Semester Exam'),
    )

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='inter'
    )
    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE_CHOICES
    )
    file = models.FileField(upload_to='examinations/')
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()} - {self.get_exam_type_display()})"




class Popup(models.Model):
    image = models.ImageField(upload_to='popups/')  
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Popup Image"