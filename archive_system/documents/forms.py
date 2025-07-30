from django import forms
from .models import Document, DocumentCategory, StorageLocation

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'document_number', 'category', 
                  'issue_date', 'expiry_date', 'storage_location', 
                  'description', 'file']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class StorageLocationForm(forms.ModelForm):
    class Meta:
        model = StorageLocation
        fields = ['name', 'room', 'shelf', 'box']

class DocumentSearchForm(forms.Form):
    query = forms.CharField(label='Пошук', required=False)
    document_type = forms.ChoiceField(
        label='Тип документа',
        choices=[('', '---')] + list(Document.DOCUMENT_TYPES),
        required=False
    )
    category = forms.ModelChoiceField(
        label='Категорія',
        queryset=DocumentCategory.objects.all(),
        required=False
    )
    start_date = forms.DateField(
        label='Дата з',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        label='Дата по',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    storage_location = forms.ModelChoiceField(
        label='Місце зберігання',
        queryset=StorageLocation.objects.all(),
        required=False
    )