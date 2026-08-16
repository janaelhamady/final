from django.contrib import admin
from .models import Instructor, Category, Course, Student, Enrollment


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')