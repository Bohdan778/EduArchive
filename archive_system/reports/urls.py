from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report-list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('new/', views.ReportCreateView.as_view(), name='report-create'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('export-csv/', views.export_documents_csv, name='export-csv'),
]