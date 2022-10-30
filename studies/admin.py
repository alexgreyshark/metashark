from django.contrib import admin
from .models import (
    AcademicGroup,
    Report,
    Student,
    StudyDirection,
    Subject,
)


@admin.register(AcademicGroup)
class AcademicGroupAdmin(admin.ModelAdmin):
    list_display = [
        'short_name',
        'study_direction',
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'sex',
        'birthday',
        'academic_group',
    ]


@admin.register(StudyDirection)
class StudyDirectionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'code',
        'curator',
    ]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'study_direction_repr',
    ]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file',
        'created_at',
        'status',
    ]
