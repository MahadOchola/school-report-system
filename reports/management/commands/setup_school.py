import os
from django.core.management.base import BaseCommand
from reports.models import School

class Command(BaseCommand):
    help = 'Create default school data'
    
    def handle(self, *args, **options):
        school, created = School.objects.get_or_create(
            name="GOMBE ISLAMIC PRIMARY SCHOOL",
            defaults={
                'address': "Gombe town \nButambala",
                'phone': "+255-123-456-789",
                'email': "info@gombeislamic.edu"
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Default school created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('School already exists'))