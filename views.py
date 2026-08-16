from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Course, Student, Enrollment, Instructor, Category
from .forms import RegisterForm, EnrollmentForm, EnrollmentEditForm


def course_list(request):
    courses = Course.objects.all()

    search = request.GET.get('search', '')
    instructor = request.GET.get('instructor', '')
    category = request.GET.get('category', '')

    if search:
        courses = courses.filter(
            Q(title__icontains=search)
        )

    if instructor:
        courses = courses.filter(
            instructor_id=instructor
        )

    if category:
        courses = courses.filter(
            category_id=category
        )

    instructors = Instructor.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        'courses/course_list.html',
        {
            'courses': courses,
            'instructors': instructors,
            'categories': categories,
            'search': search,
            'selected_instructor': instructor,
            'selected_category': category,
        }
    )


def course_detail(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id
    )

    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related('student__user')

    return render(
        request,
        'courses/course_detail.html',
        {
            'course': course,
            'enrollments': enrollments,
        }
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            Student.objects.create(
                user=user
            )

            login(request, user)

            return redirect('course_list')

    else:
        form = RegisterForm()

    return render(
        request,
        'courses/register.html',
        {
            'form': form
        }
    )


@login_required
def enroll(request):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)

        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student

            if Enrollment.objects.filter(
                student=student,
                course=enrollment.course
            ).exists():
                form.add_error(
                    'course',
                    'You are already enrolled in this course.'
                )
            else:
                enrollment.save()
                return redirect('profile')

    else:
        form = EnrollmentForm()

    return render(
        request,
        'courses/enrollment_form.html',
        {
            'form': form
        }
    )


@login_required
def edit_enrollment(request, enrollment_id):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=student
    )

    if request.method == 'POST':
        form = EnrollmentEditForm(
            request.POST,
            instance=enrollment
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EnrollmentEditForm(
            instance=enrollment
        )

    return render(
        request,
        'courses/enrollment_edit.html',
        {
            'form': form,
            'enrollment': enrollment
        }
    )
@login_required
def cancel_enrollment(request, enrollment_id):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=student
    )

    if request.method == 'POST':
        enrollment.delete()

    return redirect('profile')


@login_required
def profile(request):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related(
        'course',
        'course__instructor'
    )

    return render(
        request,
        'courses/profile.html',
        {
            'student': student,
            'enrollments': enrollments,
        }
    )


def instructor_courses(request, instructor_id):
    instructor = get_object_or_404(
        Instructor,
        id=instructor_id
    )

    courses = Course.objects.filter(
        instructor=instructor
    )

    return render(
        request,
        'courses/course_list.html',
        {
            'courses': courses,
            'instructors': Instructor.objects.all(),
            'categories': Category.objects.all(),
            'search': '',
            'selected_instructor': str(instructor_id),
            'selected_category': '',
        }
    )


@login_required
def instructor_dashboard(request):
    instructor = get_object_or_404(
        Instructor,
        user=request.user
    )

    courses = Course.objects.filter(
        instructor=instructor
    )

    return render(
        request,
        'courses/instructor_dashboard.html',
        {
            'instructor': instructor,
            'courses': courses,
        }
    )