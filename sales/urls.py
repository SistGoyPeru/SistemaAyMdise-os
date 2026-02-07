from django.urls import path
from . import views

urlpatterns = [
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer-add'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer-edit'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),

    # Orders
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/add/', views.OrderCreateView.as_view(), name='order-add'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order-edit'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
]
