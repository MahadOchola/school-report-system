from rest_framework import serializers
from .models import ClassRoom, Student, Subject, Term, Mark

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='classroom.name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    term_name = serializers.CharField(source='term.name', read_only=True)
    
    class Meta:
        model = Mark
        fields = '__all__'

class MarkInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'term', 'score']