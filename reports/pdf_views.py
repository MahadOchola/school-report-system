from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import logging
from .models import Student, Term, School
from .utils import compute_student_report

logger = logging.getLogger(__name__)

def generate_pdf_report(request, student_id, term_id):
    try:
        student = Student.objects.get(id=student_id)
        term = Term.objects.get(id=term_id)
        report = compute_student_report(student, term)
        
        # Get or create default school
        school, created = School.objects.get_or_create(
            name="Gombe islamic",
            defaults={
                'address': "gombe town\nButambala",
                'phone': "+255-123-456-789",
                'email': "info@gombeislamic.edu"
            }
        )
        
        # Render HTML template
        context = {
            'report': report,
            'student': student,
            'term': term,
            'school': school
        }
        
        html_string = render_to_string('report_template.html', context)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{student.student_id}_{term.name}.pdf"'
        
        # Generate PDF
        pdf_status = pisa.CreatePDF(
            BytesIO(html_string.encode("UTF-8")),
            dest=response,
            encoding='UTF-8'
        )
        
        if pdf_status.err:
            logger.error(f"PDF generation error: {pdf_status.err}")
            return HttpResponse('Error generating PDF. Please try again.')
            
        return response
        
    except (Student.DoesNotExist, Term.DoesNotExist):
        return HttpResponse('Student or Term not found', status=404)
    except Exception as e:
        logger.error(f"Unexpected error in PDF generation: {e}")
        return HttpResponse('An unexpected error occurred.', status=500)