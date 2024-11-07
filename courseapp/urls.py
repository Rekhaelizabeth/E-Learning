from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),
]
