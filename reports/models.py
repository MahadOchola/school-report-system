from django.db import models

import os



def school_logo_path(instance, filename):
    return f'school/logo/{filename}'

class School(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to=school_logo_path, blank=True, null=True)
    
    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    stream = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} {self.stream}" if self.stream else self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name   
    
    

    
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher_name 


        

class Term(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'subject', 'term')

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"