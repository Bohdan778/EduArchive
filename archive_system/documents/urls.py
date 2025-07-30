from django.urls import path
from . import views

urlpatterns = [
    # Документи
    path('', views.DocumentListView.as_view(), name='document-list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('new/', views.DocumentCreateView.as_view(), name='document-create'),
    path('<int:pk>/update/', views.DocumentUpdateView.as_view(), name='document-update'),
    path('<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('<int:pk>/history/', views.DocumentHistoryListView.as_view(), name='document-history'),
    
    # Категорії
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Місця зберігання
    path('locations/', views.StorageLocationListView.as_view(), name='storage-location-list'),
    path('locations/new/', views.StorageLocationCreateView.as_view(), name='storage-location-create'),
    path('locations/<int:pk>/update/', views.StorageLocationUpdateView.as_view(), name='storage-location-update'),
    path('locations/<int:pk>/delete/', views.StorageLocationDeleteView.as_view(), name='storage-location-delete'),
]