from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    
    class Meta:
        verbose_name = "Категорія документів"
        verbose_name_plural = "Категорії документів"
    
    def __str__(self):
        return self.name

class StorageLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва місця зберігання")
    room = models.CharField(max_length=50, verbose_name="Кімната")
    shelf = models.CharField(max_length=50, verbose_name="Полиця")
    box = models.CharField(max_length=50, blank=True, null=True, verbose_name="Коробка")
    
    class Meta:
        verbose_name = "Місце зберігання"
        verbose_name_plural = "Місця зберігання"
    
    def __str__(self):
        return f"{self.name} (Кімната: {self.room}, Полиця: {self.shelf})"

class Document(models.Model):
    DOCUMENT_TYPES = (
        ('diploma', 'Диплом'),
        ('certificate', 'Сертифікат'),
        ('transcript', 'Академічна довідка'),
        ('order', 'Наказ'),
        ('protocol', 'Протокол'),
        ('report', 'Звіт'),
        ('other', 'Інше'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Назва документа")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Тип документа")
    document_number = models.CharField(max_length=50, verbose_name="Номер документа")
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, verbose_name="Категорія")
    issue_date = models.DateField(verbose_name="Дата видачі")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Дата закінчення терміну дії")
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, verbose_name="Місце зберігання")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    file = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name="Файл")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_documents', verbose_name="Створено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.document_number})"
    
    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})

class DocumentHistory(models.Model):
    ACTION_TYPES = (
        ('create', 'Створення'),
        ('update', 'Оновлення'),
        ('view', 'Перегляд'),
        ('delete', 'Видалення'),
    )
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='history', verbose_name="Документ")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Користувач")
    action = models.CharField(max_length=10, choices=ACTION_TYPES, verbose_name="Дія")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Час")
    details = models.TextField(blank=True, null=True, verbose_name="Деталі")
    
    class Meta:
        verbose_name = "Історія документа"
        verbose_name_plural = "Історія документів"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_action_display()} документа {self.document.title} користувачем {self.user.username}"