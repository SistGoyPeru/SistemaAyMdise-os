from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Supply, BaseProduct, Category

from django.db.models import Q

# --- Insumos (Supplies) ---
class SupplyListView(ListView):
    model = Supply
    template_name = 'inventory/supply_list.html'
    context_object_name = 'supplies'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(name__icontains=query)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class SupplyCreateView(SuccessMessageMixin, CreateView):
    model = Supply
    template_name = 'inventory/supply_form.html'
    fields = ['name', 'category', 'unit', 'stock', 'min_stock', 'cost_per_unit']
    success_url = reverse_lazy('supply-list')
    success_message = "Insumo creado exitosamente."

class SupplyUpdateView(SuccessMessageMixin, UpdateView):
    model = Supply
    template_name = 'inventory/supply_form.html'
    fields = ['name', 'category', 'unit', 'stock', 'min_stock', 'cost_per_unit']
    success_url = reverse_lazy('supply-list')
    success_message = "Insumo actualizado exitosamente."

class SupplyDeleteView(DeleteView):
    model = Supply
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('supply-list')

# --- Productos Base ---
class BaseProductListView(ListView):
    model = BaseProduct
    template_name = 'inventory/baseproduct_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

class BaseProductCreateView(SuccessMessageMixin, CreateView):
    model = BaseProduct
    template_name = 'inventory/baseproduct_form.html'
    fields = ['name', 'category', 'description', 'stock', 'min_stock', 'cost', 'image']
    success_url = reverse_lazy('baseproduct-list')
    success_message = "Producto Base creado exitosamente."

class BaseProductUpdateView(SuccessMessageMixin, UpdateView):
    model = BaseProduct
    template_name = 'inventory/baseproduct_form.html'
    fields = ['name', 'category', 'description', 'stock', 'min_stock', 'cost', 'image']
    success_url = reverse_lazy('baseproduct-list')
    success_message = "Producto Base actualizado exitosamente."

class BaseProductDeleteView(DeleteView):
    model = BaseProduct
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('baseproduct-list')
