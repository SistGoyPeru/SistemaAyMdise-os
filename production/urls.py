from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.FinalProductListView.as_view(), name='finalproduct-list'),
    path('products/add/', views.FinalProductCreateView.as_view(), name='finalproduct-add'),
    path('products/<int:pk>/edit/', views.FinalProductUpdateView.as_view(), name='finalproduct-edit'),
    path('products/<int:pk>/', views.FinalProductDetailView.as_view(), name='finalproduct-detail'),
    path('products/<int:pk>/delete/', views.FinalProductDeleteView.as_view(), name='finalproduct-delete'),
]
