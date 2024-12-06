"""
URL configuration for USIS_5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views
from myapp.views import *

urlpatterns = [
    # |************* urls for pages index.html, about.html, contact.html, courses.html, course-details.html, events.html
    # |************* pricing.html, starter_page.html, trainers.html
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('courses/', views.courses, name='courses'),
    path('course/', views.course, name='course'),
    path('events/', views.events, name='events'),
    path('pricing/', views.pricing, name='pricing'),
    path('trainers/', views.trainers, name='trainers'),
    path('starterpage/', views.starterpage, name='starterpage'),

    #Custom URLs
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('create_assignment/', views.assignment, name='assignments'),
    path('student/dashboard/assignments/', views.view_assignments, name='view_assignments'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('lecturer/dashboard/manage_groups/', views.manage_groups, name='manage_groups'),
    path('lecturer/dashboard/manage_groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('lecturer/dashboard/manage_groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('view_group/', views.view_group, name='view_group'),  # Student dashboard
    path('join/<int:group_id>/', views.join_group, name='join_group'),  # Join a group
    path('leave/<int:group_id>/', views.leave_group, name='leave_group'),  # Leave a group
    path('group/<int:group_id>/members/', views.view_group_members, name='view_group_members'),
    path('add_timetable/', views.add_timetable, name='add_timetable'),
    path('view_timetable/', views.view_timetable, name='view_timetable'),
    path('edit_timetable/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('delete_timetable/<int:id>/', views.delete_timetable, name='delete_timetable'),
    path('sview_timetable/', views.sview_timetable, name='sview_timetable'),
    path('ssubmit_assignment/<int:assignment_id>/', views.ssubmit_assignment, name='ssubmit_assignment'),
    path('grades_dashboard/', views.grades_dashboard, name='grades_dashboard'),
    path('upload_individual_grades/<int:assignment_id>/', views.upload_individual_grades,
         name='upload_individual_grades'),
    path('upload_group_grades/<int:assignment_id>/', views.upload_group_grades, name='upload_group_grades'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.add_payment, name='add_payment'),
    #path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/initiate/<int:group_id>/', PaymentInitiateView.as_view(), name='payment_initiate'),
    path('contact/', views.contact_view, name='contact_form'),


]
