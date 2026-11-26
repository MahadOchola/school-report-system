from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .pdf_views import generate_pdf_report
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'classes', views.ClassRoomViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'terms', views.TermViewSet)
router.register(r'marks', views.MarkViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('students/', views.students_list, name='students-list'),
    path('marks/', views.enter_marks, name='enter_marks'),
    path('reports/', views.reports_view, name='reports-view'),
    path('api/', include(router.urls)),
    path('api/pdf-report/<int:student_id>/<int:term_id>/', generate_pdf_report, name='pdf-report'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)