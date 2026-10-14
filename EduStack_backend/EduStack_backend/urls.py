from django.contrib import admin
from django.urls import path
import users_app.views as user_views
import core_app.views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('api/register/', user_views.register_user, name='regsiter'),
    path('api/login/', user_views.login_user, name='login'),
    path('api/protected/', user_views.protected_view, name='protected'),

    # users
    path('api/teacher/', user_views.teacher_list, name='teacher-list'),
    path('api/teacher/<int:pk>/', user_views.teacher_detail, name='teacher-detail'),
    path('api/student/', user_views.student_list, name='student-list'),
    path('api/student/<int:pk>/', user_views.student_detail, name='student-detail'),

    # courses
    path('api/course/', core_views.course_list_create, name='course-list'),
    path('api/course/<int:pk>/', core_views.course_detail, name='course-detail'),

    # enrollments
    path('api/enrollment/', core_views.enrollment_list, name='enrollment-list'),
    path('api/enrollment/<int:pk>/', core_views.enrollment_detail, name='enrollment-detail'),

    # lessons
    path('api/lesson/', core_views.lesson_list_create, name='lesson-list'),
    path('api/lesson/<int:pk>/', core_views.lesson_detail, name='lesson-detail'),

    # assignments
    path('api/assignment/', core_views.assignment_list, name='assignment-list'),
    path('api/assignment/<int:pk>/', core_views.assignment_detail, name='assignment-detail'),

    # submissions
    path('api/submission/', core_views.submission_list, name='submission-list'),
    path('api/submission/<int:pk>/', core_views.submission_detail, name='submission-detail'),

    # results
    path('api/results/', core_views.result_list, name='result-list'),
    path('api/results/<int:pk>/', core_views.result_detail, name='result-detail'),
]
