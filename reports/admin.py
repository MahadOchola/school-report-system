from django.contrib import admin
from .models import *

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'classroom', )
    list_filter = ('classroom', 'gender')
    search_fields = ('first_name', 'last_name', 'student_id')
    
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'score')
    list_filter = ('term', 'subject')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_name','subject')
    
  