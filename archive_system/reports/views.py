from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
import csv
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from .models import Report
from .forms import ReportForm
from documents.models import Document, DocumentCategory, StorageLocation, DocumentHistory
from xhtml2pdf import pisa

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('report-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Збереження параметрів звіту
        parameters = {
            'report_type': form.cleaned_data.get('report_type'),
            'start_date': form.cleaned_data.get('start_date').isoformat() if form.cleaned_data.get('start_date') else None,
            'end_date': form.cleaned_data.get('end_date').isoformat() if form.cleaned_data.get('end_date') else None,
            'category_id': form.cleaned_data.get('category').id if form.cleaned_data.get('category') else None,
            'storage_location_id': form.cleaned_data.get('storage_location').id if form.cleaned_data.get('storage_location') else None,
            'user_id': form.cleaned_data.get('user').id if form.cleaned_data.get('user') else None,
        }
        form.instance.parameters = parameters
        
        response = super().form_valid(form)
        
        # Генерація звіту
        self.generate_report(self.object)
        
        messages.success(self.request, 'Звіт успішно створено!')
        return response
    
    def generate_report(self, report):
        report_type = report.report_type
        parameters = report.parameters
        
        if report_type == 'document_list':
            self.generate_document_list_report(report)
        elif report_type == 'document_by_category':
            self.generate_document_by_category_report(report)
        elif report_type == 'document_by_location':
            self.generate_document_by_location_report(report)
        elif report_type == 'document_by_date':
            self.generate_document_by_date_report(report)
        elif report_type == 'activity_log':
            self.generate_activity_log_report(report)
    
    def generate_document_list_report(self, report):
        # Фільтрація документів за параметрами
        queryset = Document.objects.all()
        parameters = report.parameters
        
        if parameters.get('start_date'):
            queryset = queryset.filter(issue_date__gte=parameters.get('start_date'))
        
        if parameters.get('end_date'):
            queryset = queryset.filter(issue_date__lte=parameters.get('end_date'))
        
        if parameters.get('category_id'):
            queryset = queryset.filter(category_id=parameters.get('category_id'))
        
        if parameters.get('storage_location_id'):
            queryset = queryset.filter(storage_location_id=parameters.get('storage_location_id'))
        
        # Створення PDF-звіту
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Додавання шрифту з підтримкою кирилиці
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        
        # Стилі
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.fontName = 'DejaVuSans'
        
        # Заголовок
        title = Paragraph(f"Список документів", title_style)
        elements.append(title)
        
        # Дані для таблиці
        data = [['№', 'Назва', 'Тип', 'Номер', 'Дата видачі', 'Категорія', 'Місце зберігання']]
        
        for i, doc in enumerate(queryset, 1):
            data.append([
                i,
                doc.title,
                doc.get_document_type_display(),
                doc.document_number,
                doc.issue_date.strftime('%d.%m.%Y'),
                doc.category.name if doc.category else '',
                doc.storage_location.name if doc.storage_location else ''
            ])
        
        # Створення таблиці
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Збереження PDF
        doc.build(elements)
        
        # Збереження файлу звіту
        filename = f"document_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report.file.save(filename, BytesIO(buffer.getvalue()))
    
    def generate_document_by_category_report(self, report):
        # Аналогічно до generate_document_list_report, але з групуванням за категоріями
        pass
    
    def generate_document_by_location_report(self, report):
        # Аналогічно до generate_document_list_report, але з групуванням за місцями зберігання
        pass
    
    def generate_document_by_date_report(self, report):
        # Аналогічно до generate_document_list_report, але з групуванням за датами
        pass
    
    def generate_activity_log_report(self, report):
        # Звіт з історії активності
        pass

class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Report
    template_name = 'reports/report_confirm_delete.html'
    success_url = reverse_lazy('report-list')
    
    def test_func(self):
        report = self.get_object()
        return self.request.user == report.created_by or self.request.user.is_staff

@login_required
def export_documents_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="documents_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Назва', 'Тип', 'Номер', 'Дата видачі', 'Категорія', 'Місце зберігання', 'Опис'])
    
    documents = Document.objects.all()
    for doc in documents:
        writer.writerow([
            doc.title,
            doc.get_document_type_display(),
            doc.document_number,
            doc.issue_date.strftime('%d.%m.%Y'),
            doc.category.name if doc.category else '',
            doc.storage_location.name if doc.storage_location else '',
            doc.description
        ])
    
    return response

# Функція для перетворення HTML в PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None