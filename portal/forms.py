from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CandidateProfile, CompanyProfile, JobPost, JobApplication, Interview, ContactMessage


# ─── AUTH FORMS ──────────────────────────────────────────────────────────────

class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    skills = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, HTML'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Company Email'}))

    class Meta:
        model = User
        fields = ['company_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


# ─── CANDIDATE PROFILE FORM ───────────────────────────────────────────────────

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['phone', 'location', 'skills', 'education', 'experience', 'resume', 'profile_picture', 'bio', 'linkedin', 'github']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, React...'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'B.Tech Computer Science, XYZ University, 2024'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Software Developer at ABC Corp, 2022-2024'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ─── COMPANY PROFILE FORM ────────────────────────────────────────────────────

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'description', 'website', 'location', 'industry', 'company_size', 'logo', 'phone']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Information Technology'}),
            'company_size': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ─── JOB POST FORM ───────────────────────────────────────────────────────────

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'required_skills', 'location', 'salary_min', 'salary_max', 'job_type', 'experience_required', 'vacancies', 'deadline', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mumbai, Remote'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Salary (₹)'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Salary (₹)'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_required': forms.Select(attrs={'class': 'form-select'}),
            'vacancies': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ─── JOB APPLICATION FORM ────────────────────────────────────────────────────

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your cover letter...'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ─── INTERVIEW FORM ──────────────────────────────────────────────────────────

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['scheduled_date', 'mode', 'location_or_link', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'location_or_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meeting link or address'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ─── CONTACT FORM ────────────────────────────────────────────────────────────

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message...'}),
        }


# ─── JOB SEARCH FORM ─────────────────────────────────────────────────────────

class JobSearchForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title or Keywords'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}))
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}))
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + JobPost.JOB_TYPE_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select'}))


# ─── CANDIDATE SEARCH FORM ──────────────────────────────────────────────────

class CandidateSearchForm(forms.Form):
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by skills...'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}))
