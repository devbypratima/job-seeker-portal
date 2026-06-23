from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import (UserProfile, CandidateProfile, CompanyProfile,
                     JobPost, JobApplication, Interview, ContactMessage)
from .forms import (CandidateRegistrationForm, CompanyRegistrationForm, LoginForm,
                    CandidateProfileForm, CompanyProfileForm, JobPostForm,
                    JobApplicationForm, InterviewForm, ContactForm,
                    JobSearchForm, CandidateSearchForm)


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_user_role(user):
    try:
        return user.profile.role
    except Exception:
        return None


# ─── HOME ─────────────────────────────────────────────────────────────────────

def home(request):
    recent_jobs = JobPost.objects.filter(is_active=True).select_related('company').order_by('-created_at')[:6]
    total_jobs = JobPost.objects.filter(is_active=True).count()
    total_candidates = CandidateProfile.objects.count()
    total_companies = CompanyProfile.objects.count()
    return render(request, 'home.html', {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'total_candidates': total_candidates,
        'total_companies': total_companies,
    })


# ─── ABOUT / CONTACT ─────────────────────────────────────────────────────────

def about(request):
    return render(request, 'about.html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})


# ─── CHOICE PAGES ────────────────────────────────────────────────────────────

def register_choice(request):
    """Landing page – choose Candidate or Company registration."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'register.html')


def login_choice(request):
    """Landing page – choose Candidate or Company login."""
    if request.user.is_authenticated:
        role = get_user_role(request.user)
        if role == 'candidate':
            return redirect('candidate_dashboard')
        elif role == 'company':
            return redirect('company_dashboard')
        return redirect('home')
    return render(request, 'login_choice.html')


def candidate_login(request):
    """Login form specifically for candidates."""
    if request.user.is_authenticated:
        return redirect('candidate_dashboard')
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            role = get_user_role(user)
            if role != 'candidate' and not user.is_staff:
                messages.error(request, 'This account is not a candidate account. Please use Company Login.')
                return render(request, 'candidate/login.html', {'form': form})
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 🎉')
            return redirect('candidate_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'candidate/login.html', {'form': form})


def company_login(request):
    """Login form specifically for companies."""
    if request.user.is_authenticated:
        return redirect('company_dashboard')
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            role = get_user_role(user)
            if role != 'company' and not user.is_staff:
                messages.error(request, 'This account is not a company account. Please use Candidate Login.')
                return render(request, 'company/login.html', {'form': form})
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! 🏢')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('company_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'company/login.html', {'form': form})


# ─── CANDIDATE AUTH ──────────────────────────────────────────────────────────

def candidate_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CandidateRegistrationForm()
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            UserProfile.objects.create(user=user, role='candidate')
            CandidateProfile.objects.create(user=user, skills=form.cleaned_data.get('skills', ''))
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your candidate account is created. 🎉')
            return redirect('candidate_dashboard')
    return render(request, 'candidate/register.html', {'form': form})


def company_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CompanyRegistrationForm()
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(user=user, role='company')
            CompanyProfile.objects.create(user=user, company_name=form.cleaned_data['company_name'])
            login(request, user)
            messages.success(request, 'Company account created successfully! 🏢')
            return redirect('company_dashboard')
    return render(request, 'company/register.html', {'form': form})


def user_login(request):
    """Generic login – used as fallback / for @login_required redirects."""
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            role = get_user_role(user)
            if role == 'candidate':
                return redirect('candidate_dashboard')
            elif role == 'company':
                return redirect('company_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login_choice.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you soon!')
    return redirect('login_choice')


# ─── CANDIDATE VIEWS ─────────────────────────────────────────────────────────

@login_required
def candidate_dashboard(request):
    """Candidate's main home after login – stats + quick actions."""
    if get_user_role(request.user) != 'candidate':
        messages.error(request, 'Access denied.')
        return redirect('home')
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    applications = JobApplication.objects.filter(candidate=profile).select_related('job', 'job__company')
    total_applied = applications.count()
    shortlisted = applications.filter(status='shortlisted').count()
    interviews = applications.filter(status__in=['shortlisted']).filter(interview__isnull=False).count()
    hired = applications.filter(status='hired').count()
    recent_apps = applications[:5]
    recent_jobs = JobPost.objects.filter(is_active=True).select_related('company').order_by('-created_at')[:4]
    return render(request, 'candidate/dashboard.html', {
        'profile': profile,
        'total_applied': total_applied,
        'shortlisted': shortlisted,
        'interviews': interviews,
        'hired': hired,
        'recent_apps': recent_apps,
        'recent_jobs': recent_jobs,
    })


@login_required
def candidate_profile(request):
    role = get_user_role(request.user)
    if role != 'candidate':
        messages.error(request, 'Access denied.')
        return redirect('home')
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    form = CandidateProfileForm(instance=profile)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('candidate_profile')
    applications = JobApplication.objects.filter(candidate=profile).select_related('job', 'job__company')
    return render(request, 'candidate/profile.html', {
        'form': form,
        'profile': profile,
        'applications': applications,
    })


@login_required
def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = JobPost.objects.filter(is_active=True).select_related('company')
    if form.is_valid():
        title = form.cleaned_data.get('title')
        location = form.cleaned_data.get('location')
        skills = form.cleaned_data.get('skills')
        job_type = form.cleaned_data.get('job_type')
        if title:
            jobs = jobs.filter(Q(title__icontains=title) | Q(description__icontains=title))
        if location:
            jobs = jobs.filter(location__icontains=location)
        if skills:
            jobs = jobs.filter(required_skills__icontains=skills)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
    return render(request, 'candidate/job_search.html', {'form': form, 'jobs': jobs})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, is_active=True)
    already_applied = False
    if get_user_role(request.user) == 'candidate':
        try:
            candidate = request.user.candidate_profile
            already_applied = JobApplication.objects.filter(job=job, candidate=candidate).exists()
        except CandidateProfile.DoesNotExist:
            pass
    return render(request, 'candidate/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
    })


@login_required
def apply_job(request, job_id):
    if get_user_role(request.user) != 'candidate':
        messages.error(request, 'Only candidates can apply for jobs.')
        return redirect('home')
    job = get_object_or_404(JobPost, id=job_id, is_active=True)
    candidate = get_object_or_404(CandidateProfile, user=request.user)
    if JobApplication.objects.filter(job=job, candidate=candidate).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    form = JobApplicationForm()
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = candidate
            application.save()
            messages.success(request, f'Successfully applied for "{job.title}"!')
            return redirect('candidate_profile')
    return render(request, 'candidate/apply.html', {'form': form, 'job': job})


# ─── COMPANY VIEWS ───────────────────────────────────────────────────────────

@login_required
def company_dashboard(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')
    company = get_object_or_404(CompanyProfile, user=request.user)
    jobs = JobPost.objects.filter(company=company).order_by('-created_at')
    total_applications = JobApplication.objects.filter(job__company=company).count()
    interviews = Interview.objects.filter(application__job__company=company).count()
    return render(request, 'company/dashboard.html', {
        'company': company,
        'jobs': jobs,
        'total_applications': total_applications,
        'interviews': interviews,
    })


@login_required
def company_profile(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')
    profile, _ = CompanyProfile.objects.get_or_create(user=request.user, defaults={'company_name': request.user.username})
    form = CompanyProfileForm(instance=profile)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated!')
            return redirect('company_dashboard')
    return render(request, 'company/profile.html', {'form': form, 'profile': profile})


@login_required
def post_job(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')
    company = get_object_or_404(CompanyProfile, user=request.user)
    form = JobPostForm()
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('company_dashboard')
    return render(request, 'company/post_job.html', {'form': form})


@login_required
def edit_job(request, job_id):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(JobPost, id=job_id, company=company)
    form = JobPostForm(instance=job)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('company_dashboard')
    return render(request, 'company/post_job.html', {'form': form, 'edit': True, 'job': job})


@login_required
def delete_job(request, job_id):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(JobPost, id=job_id, company=company)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('company_dashboard')
    return render(request, 'company/confirm_delete.html', {'job': job})


@login_required
def view_applications(request, job_id):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(JobPost, id=job_id, company=company)
    applications = JobApplication.objects.filter(job=job).select_related('candidate', 'candidate__user')
    return render(request, 'company/applications.html', {'job': job, 'applications': applications})


@login_required
def update_application_status(request, app_id):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    application = get_object_or_404(JobApplication, id=app_id, job__company__user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(JobApplication.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, f'Application status updated to {status}.')
    return redirect('view_applications', job_id=application.job.id)


@login_required
def schedule_interview(request, app_id):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    application = get_object_or_404(JobApplication, id=app_id, job__company__user=request.user)
    form = InterviewForm()
    if hasattr(application, 'interview'):
        form = InterviewForm(instance=application.interview)
    if request.method == 'POST':
        if hasattr(application, 'interview'):
            form = InterviewForm(request.POST, instance=application.interview)
        else:
            form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            application.status = 'shortlisted'
            application.save()
            messages.success(request, 'Interview scheduled successfully!')
            return redirect('view_applications', job_id=application.job.id)
    return render(request, 'company/schedule_interview.html', {'form': form, 'application': application})


@login_required
def search_candidates(request):
    if get_user_role(request.user) != 'company':
        return redirect('home')
    form = CandidateSearchForm(request.GET or None)
    candidates = CandidateProfile.objects.select_related('user').all()
    if form.is_valid():
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        if skills:
            candidates = candidates.filter(skills__icontains=skills)
        if location:
            candidates = candidates.filter(location__icontains=location)
    return render(request, 'company/search_candidates.html', {'form': form, 'candidates': candidates})


# ─── ADMIN VIEWS ─────────────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'Admin access required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    context = {
        'total_candidates': CandidateProfile.objects.count(),
        'total_companies': CompanyProfile.objects.count(),
        'total_jobs': JobPost.objects.count(),
        'active_jobs': JobPost.objects.filter(is_active=True).count(),
        'total_applications': JobApplication.objects.count(),
        'total_interviews': Interview.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_jobs': JobPost.objects.order_by('-created_at')[:5],
        'recent_applications': JobApplication.objects.order_by('-applied_at')[:5],
    }
    return render(request, 'admin_portal/dashboard.html', context)


@admin_required
def admin_candidates(request):
    candidates = CandidateProfile.objects.select_related('user').order_by('-user__date_joined')
    return render(request, 'admin_portal/candidates.html', {'candidates': candidates})


@admin_required
def admin_companies(request):
    companies = CompanyProfile.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin_portal/companies.html', {'companies': companies})


@admin_required
def admin_verify_company(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    company.is_verified = not company.is_verified
    company.save()
    status = 'verified' if company.is_verified else 'unverified'
    messages.success(request, f'{company.company_name} has been {status}.')
    return redirect('admin_companies')


@admin_required
def admin_jobs(request):
    jobs = JobPost.objects.select_related('company').order_by('-created_at')
    return render(request, 'admin_portal/jobs.html', {'jobs': jobs})


@admin_required
def admin_toggle_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.is_active = not job.is_active
    job.save()
    messages.success(request, f'Job "{job.title}" {"activated" if job.is_active else "deactivated"}.')
    return redirect('admin_jobs')


@admin_required
def admin_delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.delete()
    messages.success(request, 'Job deleted.')
    return redirect('admin_jobs')


@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted.')
    return redirect('admin_candidates')


@admin_required
def admin_applications(request):
    applications = JobApplication.objects.select_related('job', 'job__company', 'candidate', 'candidate__user').order_by('-applied_at')
    return render(request, 'admin_portal/applications.html', {'applications': applications})


@admin_required
def admin_interviews(request):
    interviews = Interview.objects.select_related('application', 'application__job', 'application__candidate', 'application__candidate__user').order_by('-scheduled_date')
    return render(request, 'admin_portal/interviews.html', {'interviews': interviews})


@admin_required
def admin_messages(request):
    contact_msgs = ContactMessage.objects.order_by('-created_at')
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'admin_portal/messages.html', {'messages_list': contact_msgs})
