from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Document, DocumentCategory, StorageLocation, DocumentHistory
from .forms import DocumentForm, DocumentCategoryForm, StorageLocationForm, DocumentSearchForm

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = DocumentSearchForm(self.request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            document_type = form.cleaned_data.get('document_type')
            category = form.cleaned_data.get('category')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            storage_location = form.cleaned_data.get('storage_location')
            
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | 
                    Q(document_number__icontains=query) |
                    Q(description__icontains=query)
                )
            
            if document_type:
                queryset = queryset.filter(document_type=document_type)
            
            if category:
                queryset = queryset.filter(category=category)
            
            if start_date:
                queryset = queryset.filter(issue_date__gte=start_date)
            
            if end_date:
                queryset = queryset.filter(issue_date__lte=end_date)
            
            if storage_location:
                queryset = queryset.filter(storage_location=storage_location)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DocumentSearchForm(self.request.GET)
        return context

class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Записуємо історію перегляду
        DocumentHistory.objects.create(
            document=obj,
            user=self.request.user,
            action='view',
            details=f'Перегляд документа користувачем {self.request.user.username}'
        )
        return obj

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Записуємо історію створення
        DocumentHistory.objects.create(
            document=self.object,
            user=self.request.user,
            action='create',
            details=f'Створення документа користувачем {self.request.user.username}'
        )
        
        messages.success(self.request, 'Документ успішно створено!')
        return response

class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Записуємо історію оновлення
        DocumentHistory.objects.create(
            document=self.object,
            user=self.request.user,
            action='update',
            details=f'Оновлення документа користувачем {self.request.user.username}'
        )
        
        messages.success(self.request, 'Документ успішно оновлено!')
        return response
    
    def test_func(self):
        document = self.get_object()
        return self.request.user == document.created_by or self.request.user.is_staff

class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('document-list')
    
    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        
        # Записуємо історію видалення
        DocumentHistory.objects.create(
            document=document,
            user=self.request.user,
            action='delete',
            details=f'Видалення документа користувачем {self.request.user.username}'
        )
        
        messages.success(request, 'Документ успішно видалено!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        document = self.get_object()
        return self.request.user == document.created_by or self.request.user.is_staff

# Представлення для категорій документів
class CategoryListView(LoginRequiredMixin, ListView):
    model = DocumentCategory
    template_name = 'documents/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = DocumentCategory
    form_class = DocumentCategoryForm
    template_name = 'documents/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категорію успішно створено!')
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = DocumentCategory
    form_class = DocumentCategoryForm
    template_name = 'documents/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категорію успішно оновлено!')
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DocumentCategory
    template_name = 'documents/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    
    def test_func(self):
        return self.request.user.is_staff

# Представлення для місць зберігання
class StorageLocationListView(LoginRequiredMixin, ListView):
    model = StorageLocation
    template_name = 'documents/storage_location_list.html'
    context_object_name = 'locations'

class StorageLocationCreateView(LoginRequiredMixin, CreateView):
    model = StorageLocation
    form_class = StorageLocationForm
    template_name = 'documents/storage_location_form.html'
    success_url = reverse_lazy('storage-location-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Місце зберігання успішно створено!')
        return super().form_valid(form)

class StorageLocationUpdateView(LoginRequiredMixin, UpdateView):
    model = StorageLocation
    form_class = StorageLocationForm
    template_name = 'documents/storage_location_form.html'
    success_url = reverse_lazy('storage-location-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Місце зберігання успішно оновлено!')
        return super().form_valid(form)

class StorageLocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StorageLocation
    template_name = 'documents/storage_location_confirm_delete.html'
    success_url = reverse_lazy('storage-location-list')
    
    def test_func(self):
        return self.request.user.is_staff

# Представлення для історії документів
class DocumentHistoryListView(LoginRequiredMixin, ListView):
    model = DocumentHistory
    template_name = 'documents/document_history_list.html'
    context_object_name = 'history'
    paginate_by = 20
    
    def get_queryset(self):
        document_id = self.kwargs.get('pk')
        return DocumentHistory.objects.filter(document_id=document_id).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_id = self.kwargs.get('pk')
        context['document'] = get_object_or_404(Document, pk=document_id)
        return context