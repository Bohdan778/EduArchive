from django import forms
from django.contrib.auth.models import User
from documents.models import DocumentCategory, StorageLocation
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_type']
    
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
    category = forms.ModelChoiceField(
        label='Категорія',
        queryset=DocumentCategory.objects.all(),
        required=False
    )
    storage_location = forms.ModelChoiceField(
        label='Місце зберігання',
        queryset=StorageLocation.objects.all(),
        required=False
    )
    user = forms.ModelChoiceField(
        label='Користувач',
        queryset=User.objects.all(),
        required=False
    )