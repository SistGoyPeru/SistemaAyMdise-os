from django.urls import path
from . import views

urlpatterns = [
    # Insumos
    path('supplies/', views.SupplyListView.as_view(), name='supply-list'),
    path('supplies/add/', views.SupplyCreateView.as_view(), name='supply-add'),
    path('supplies/<int:pk>/edit/', views.SupplyUpdateView.as_view(), name='supply-edit'),
    path('supplies/<int:pk>/delete/', views.SupplyDeleteView.as_view(), name='supply-delete'),
    
    # Productos Base
    path('base-products/', views.BaseProductListView.as_view(), name='baseproduct-list'),
    path('base-products/add/', views.BaseProductCreateView.as_view(), name='baseproduct-add'),
    path('base-products/<int:pk>/edit/', views.BaseProductUpdateView.as_view(), name='baseproduct-edit'),
    path('base-products/<int:pk>/delete/', views.BaseProductDeleteView.as_view(), name='baseproduct-delete'),
]
