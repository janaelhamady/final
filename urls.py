from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path(
        '',
        views.course_list,
        name='course_list'
    ),

    path(
        'course/<int:course_id>/',
        views.course_detail,
        name='course_detail'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='courses/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'enroll/',
        views.enroll,
        name='enroll'
    ),

    path(
        'enrollment/<int:enrollment_id>/edit/',
        views.edit_enrollment,
        name='edit_enrollment'
    ),

    path(
        'enrollment/<int:enrollment_id>/cancel/',
        views.cancel_enrollment,
        name='cancel_enrollment'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'instructor/<int:instructor_id>/',
        views.instructor_courses,
        name='instructor_courses'
    ),
    path(
    'instructor-dashboard/',
    views.instructor_dashboard,
    name='instructor_dashboard'
),
]