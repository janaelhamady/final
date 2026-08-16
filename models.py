from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='instructor'
    )

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student'
    )

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def __str__(self):
        return f'{self.student} - {self.course}'