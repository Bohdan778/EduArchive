from django.contrib import admin
from .models import Document, DocumentCategory, StorageLocation, DocumentHistory

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'document_number', 'issue_date', 'category', 'storage_location', 'created_by', 'created_at')
    list_filter = ('document_type', 'category', 'storage_location', 'issue_date', 'created_at')
    search_fields = ('title', 'document_number', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'shelf', 'box')
    search_fields = ('name', 'room', 'shelf', 'box')

@admin.register(DocumentHistory)
class DocumentHistoryAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('document__title', 'user__username', 'details')
    date_hierarchy = 'timestamp'
    readonly_fields = ('document', 'user', 'action', 'timestamp', 'details')