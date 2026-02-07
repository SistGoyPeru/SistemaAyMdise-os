from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db import transaction
from .models import Order, Customer
from .forms import OrderForm, OrderItemFormSet, CustomerForm

# --- Customers ---
class CustomerListView(ListView):
    model = Customer
    template_name = 'sales/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('customer-list')
    success_message = "Cliente registrado exitosamente."

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('customer-list')
    success_message = "Cliente actualizado exitosamente."

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('customer-list')

from django.db.models import Q

# --- Orders ---
class OrderListView(ListView):
    model = Order
    template_name = 'sales/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Search by ID or Customer Name
            queryset = queryset.filter(
                Q(id__icontains=query) | 
                Q(customer__name__icontains=query)
            )
        return queryset

class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'sales/order_form.html'
    success_url = reverse_lazy('order-list')
    success_message = "Pedido creado exitosamente."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = OrderItemFormSet(self.request.POST)
        else:
            data['items_formset'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if form.is_valid() and items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.instance = self.object
                items_formset.save()
                # Calculate total after saving items
                self.object.calculate_total()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'sales/order_form.html'
    success_url = reverse_lazy('order-list')
    success_message = "Pedido actualizado exitosamente."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['items_formset'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if form.is_valid() and items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.save()
                self.object.calculate_total()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderDetailView(DetailView):
    model = Order
    template_name = 'sales/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        
        # Calcular materiales totales
        materials_needed = {} # {supply_name: {quantity: X, unit: U}}
        base_products_needed = {} # {product_name: {quantity: X}}

        for item in order.items.all():
            final_product = item.product
            qty = item.quantity

            # 1. Producto Base
            bp = final_product.base_product
            if bp.name in base_products_needed:
                base_products_needed[bp.name]['quantity'] += qty
            else:
                base_products_needed[bp.name] = {'quantity': qty}

            # 2. Insumos (BOM)
            for bom in final_product.billofmaterial_set.all():
                supply = bom.supply
                total_qty = bom.quantity * qty
                
                if supply.name in materials_needed:
                    materials_needed[supply.name]['quantity'] += total_qty
                else:
                    materials_needed[supply.name] = {
                        'quantity': total_qty,
                        'unit': supply.unit.abbreviation
                    }
        
        context['materials_needed'] = materials_needed
        context['base_products_needed'] = base_products_needed
        return context

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('order-list')
