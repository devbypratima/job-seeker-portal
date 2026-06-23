from django.db import models
from django.contrib.auth.models import User


# ─── USER ROLES ──────────────────────────────────────────────────────────────

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('company', 'Company'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ─── CANDIDATE ───────────────────────────────────────────────────────────────

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='candidate_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Candidate"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


# ─── COMPANY ─────────────────────────────────────────────────────────────────

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True,
        choices=[('1-10','1-10'),('11-50','11-50'),('51-200','51-200'),
                 ('201-500','201-500'),('500+','500+')])
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# ─── JOB POST ─────────────────────────────────────────────────────────────────

class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('remote', 'Remote'),
    ]
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('1-2', '1-2 Years'),
        ('3-5', '3-5 Years'),
        ('5-10', '5-10 Years'),
        ('10+', '10+ Years'),
    ]

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills")
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    vacancies = models.PositiveIntegerField(default=1)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

    def get_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]


# ─── JOB APPLICATION ─────────────────────────────────────────────────────────

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'candidate']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.user.username} → {self.job.title}"


# ─── INTERVIEW ────────────────────────────────────────────────────────────────

class Interview(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
        ('phone', 'Phone'),
    ]
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='interview')
    scheduled_date = models.DateTimeField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='online')
    location_or_link = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview: {self.application.candidate.user.username} for {self.application.job.title}"


# ─── CONTACT ─────────────────────────────────────────────────────────────────

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
