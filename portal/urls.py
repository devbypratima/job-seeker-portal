from django.urls import path
from . import views

urlpatterns = [
    # ── General ──────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ── Auth Choice Pages ─────────────────────
    path('register/', views.register_choice, name='register'),
    path('login/', views.login_choice, name='login_choice'),
    path('login/', views.login_choice, name='login'),       # backward-compat alias
    path('login/candidate/', views.candidate_login, name='candidate_login'),
    path('login/company/', views.company_login, name='company_login'),
    path('logout/', views.user_logout, name='logout'),

    # ── Registration Forms ────────────────────
    path('register/candidate/', views.candidate_register, name='candidate_register'),
    path('register/company/', views.company_register, name='company_register'),

    # ── Candidate ────────────────────────────
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('jobs/', views.job_search, name='job_search'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),

    # ── Company ──────────────────────────────
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('company/profile/', views.company_profile, name='company_profile'),
    path('company/post-job/', views.post_job, name='post_job'),
    path('company/jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('company/jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('company/jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('company/applications/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
    path('company/applications/<int:app_id>/interview/', views.schedule_interview, name='schedule_interview'),
    path('company/candidates/', views.search_candidates, name='search_candidates'),

    # ── Admin Portal ─────────────────────────
    path('admin-portal/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-portal/candidates/', views.admin_candidates, name='admin_candidates'),
    path('admin-portal/candidates/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-portal/companies/', views.admin_companies, name='admin_companies'),
    path('admin-portal/companies/<int:company_id>/verify/', views.admin_verify_company, name='admin_verify_company'),
    path('admin-portal/jobs/', views.admin_jobs, name='admin_jobs'),
    path('admin-portal/jobs/<int:job_id>/toggle/', views.admin_toggle_job, name='admin_toggle_job'),
    path('admin-portal/jobs/<int:job_id>/delete/', views.admin_delete_job, name='admin_delete_job'),
    path('admin-portal/applications/', views.admin_applications, name='admin_applications'),
    path('admin-portal/interviews/', views.admin_interviews, name='admin_interviews'),
    path('admin-portal/messages/', views.admin_messages, name='admin_messages'),
]
