def grade_from_score(score):
    """Convert a numerical score to a letter grade."""
    if score >= 90:
        return 'A'
    if score >= 80:
        return 'B'
    if score >= 70:
        return 'C'
    if score >= 60:
        return 'D'
    return 'F'

def compute_student_report(student, term ):
    """Return per-subject grades and overall totals for a student in a term."""
    marks = student.marks.filter(term=term).select_related('subject')
    total = 0
    count = 0
    subjects = []
    for m in marks:
        total += float(m.score)
        count += 1
        subjects.append({
            'subject': m.subject.name,
            'score': float(m.score),
            'grade': grade_from_score(float(m.score)),
        })
    average = total / count if count else 0
    overall_grade = grade_from_score(average)
    return {
        'student': str(student),
        'subjects': subjects,
        'total': total,
        'average': average,
        'overall_grade': overall_grade,
    }
    