from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = (
        ('document_list', 'Список документів'),
        ('document_by_category', 'Документи за категоріями'),
        ('document_by_location', 'Документи за місцем зберігання'),
        ('document_by_date', 'Документи за датою'),
        ('activity_log', 'Журнал активності'),
        ('custom', 'Користувацький звіт'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Назва звіту")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name="Тип звіту")
    parameters = models.JSONField(blank=True, null=True, verbose_name="Параметри")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Створено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    file = models.FileField(upload_to='reports/', blank=True, null=True, verbose_name="Файл звіту")
    
    class Meta:
        verbose_name = "Звіт"
        verbose_name_plural = "Звіти"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title