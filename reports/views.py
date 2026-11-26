from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv
from .models import *
from .serializers import *
from .utils import compute_student_report
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import json

def index(request):
    """Home page with overview"""
    # Get some statistics for the dashboard
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_terms = Term.objects.count()
    
    # Get recent activities (example implementation)
    recent_activities = []
    
    # Add recent student registrations
    recent_students = Student.objects.order_by('-id')[:3]
    for student in recent_students:
        recent_activities.append({
            'icon': 'fa-user-plus',
            'message': f'New student registered: {student.first_name} {student.last_name}',
            'time': 'Recently'
        })
    
    # Add recent marks entries
    recent_marks = Mark.objects.select_related('student', 'subject').order_by('-id')[:2]
    for mark in recent_marks:
        recent_activities.append({
            'icon': 'fa-edit',
            'message': f'Marks updated for {mark.student.first_name} in {mark.subject.name}',
            'time': 'Recently'
        })
    
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_terms': total_terms,
        'recent_activities': recent_activities,
    }
    return render(request, 'index.html', context)

def reports_view(request):
    """Display student reports - THE MISSING FUNCTION"""
    students = Student.objects.all().select_related('classroom')
    terms = Term.objects.all().order_by('-year', 'name')
    
    # Get filter parameters
    student_id = request.GET.get('student')
    term_id = request.GET.get('term')
    
    
    reports = []
    selected_student = None
    selected_term = None
    
    if student_id and term_id:
        try:
            selected_student = Student.objects.get(id=student_id)
            selected_term = Term.objects.get(id=term_id)
            
            # Generate report using your utility function
            report_data = compute_student_report(selected_student, selected_term)
            reports = [report_data]  # Wrap in list for template iteration
            
        except (Student.DoesNotExist, Term.DoesNotExist):
            messages.error(request, 'Student or Term not found')
    
    context = {
        'students': students,
        'terms': terms,
        'reports': reports,
        'selected_student': selected_student,
        'selected_term': selected_term,
       
    }
    return render(request, 'reports.html', context)

def students_list(request):
    """Display all students"""
    students = Student.objects.all().select_related('classroom')
    classrooms = ClassRoom.objects.all()
    
    context = {
        'students': students,
        'classrooms': classrooms,
    }
    return render(request, 'students.html', context)

def enter_marks(request):
    if request.method == 'POST':
        try:
            # Get data from the form
            student_id = request.POST.get('student')
            subject_id = request.POST.get('subject')
            term_id = request.POST.get('term')
            score = request.POST.get('score')
            teacher_id = request.POST.get('teacher')
            
            # Validate required fields
            if not all([student_id, subject_id, term_id, score]):
                messages.error(request, 'All fields are required')
                return redirect('enter_marks')
            
            # Convert score to float
            try:
                score = float(score)
            except ValueError:
                messages.error(request, 'Score must be a valid number')
                return redirect('enter_marks')
            
            # Check if score is within valid range
            if score < 0 or score > 100:
                messages.error(request, 'Score must be between 0 and 100')
                return redirect('enter_marks')
            
            # Get objects
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            term = Term.objects.get(id=term_id)
            
            # Check if mark already exists for this student, subject, and term
            mark, created = Mark.objects.get_or_create(
                student=student,
                subject=subject,
                term=term,
                defaults={'score': score}
            )
            
            if not created:
                # Update existing mark
                mark.score = score
                mark.save()
                messages.success(request, f'Mark updated for {student.first_name} in {subject.name}')
            else:
                messages.success(request, f'Mark added for {student.first_name} in {subject.name}')
                
        except Student.DoesNotExist:
            messages.error(request, 'Student not found')
        except Subject.DoesNotExist:
            messages.error(request, 'Subject not found')
        except Term.DoesNotExist:
            messages.error(request, 'Term not found')
        except Exception as e:
            messages.error(request, f'Error saving mark: {str(e)}')
        
        return redirect('enter_marks')
    
    else:
        # GET request - show the form
        students = Student.objects.all().order_by('first_name')
        subjects = Subject.objects.all().order_by('name')
        terms = Term.objects.all().order_by('-year', 'name')
        
        context = {
            'students': students,
            'subjects': subjects,
            'terms': terms,
        }
        return render(request, 'marks.html', context)

# API ViewSets
class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('classroom')
    serializer_class = StudentSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all().select_related('student', 'subject', 'term')
    serializer_class = MarkSerializer

    def create(self, request, *args, **kwargs):
        serializer = MarkInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def student_report(self, request):
        student_id = request.query_params.get('student_id')
        term_id = request.query_params.get('term_id')
        
        if not student_id or not term_id:
            return Response({'error': 'student_id and term_id are required'}, status=400)
        
        try:
            student = Student.objects.get(id=student_id)
            term = Term.objects.get(id=term_id)
            report = compute_student_report(student, term)
            return Response(report)
        except (Student.DoesNotExist, Term.DoesNotExist):
            return Response({'error': 'Student or Term not found'}, status=404)

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({'error': 'No file provided'}, status=400)
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            imported_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, 2):
                try:
                    student_id = row.get('student_id')
                    subject_name = row.get('subject')
                    term_name = row.get('term')
                    score = row.get('score')
                    
                    if not all([student_id, subject_name, term_name, score]):
                        errors.append(f"Row {row_num}: Missing required fields")
                        continue
                    
                    student = Student.objects.get(student_id=student_id)
                    subject, _ = Subject.objects.get_or_create(name=subject_name)
                    term, _ = Term.objects.get_or_create(name=term_name, year=2025)
                    
                    mark, created = Mark.objects.update_or_create(
                        student=student,
                        subject=subject,
                        term=term,
                        defaults={'score': score}
                    )
                    
                    if created:
                        imported_count += 1
                        
                except Student.DoesNotExist:
                    errors.append(f"Row {row_num}: Student with ID {student_id} not found")
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
            
            return Response({
                'imported_count': imported_count,
                'errors': errors
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="marks_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Student Name', 'Subject', 'Term', 'Score', 'Grade', 'Teacher'])
        
        marks = Mark.objects.all().select_related('student', 'subject', 'term')
        for mark in marks:
            grade = 'A' if float(mark.score) >= 90 else 'B' if float(mark.score) >= 80 else 'C' if float(mark.score) >= 70 else 'D' if float(mark.score) >= 60 else 'F'
            writer.writerow([
                mark.student.student_id,
                f"{mark.student.first_name} {mark.student.last_name}",
                mark.subject.name,
                mark.term.name,
                mark.score,
                grade
            ])
        
        return response