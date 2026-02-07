from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db import transaction
from .models import FinalProduct
from .forms import FinalProductForm, BOMFormSet

class FinalProductListView(ListView):
    model = FinalProduct
    template_name = 'production/finalproduct_list.html'
    context_object_name = 'products'

class FinalProductCreateView(SuccessMessageMixin, CreateView):
    model = FinalProduct
    form_class = FinalProductForm
    template_name = 'production/finalproduct_form.html'
    success_url = reverse_lazy('finalproduct-list')
    success_message = "Producto Final creado exitosamente."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['bom_formset'] = BOMFormSet(self.request.POST)
        else:
            data['bom_formset'] = BOMFormSet()
        
        # Data for Simulator (JS)
        from inventory.models import BaseProduct, Supply
        import json
        
        # Base Products: id -> {cost: float, image: url}
        bp_data = {}
        for bp in BaseProduct.objects.all():
            bp_data[bp.id] = {
                'cost': float(bp.cost.amount),
                'image': bp.image.url if bp.image else '',
                'name': bp.name
            }
        
        # Supplies: id -> {cost: float, unit: str}
        supply_data = {}
        for s in Supply.objects.all():
            supply_data[s.id] = {
                'cost': float(s.cost_per_unit.amount),
                'unit': s.unit.abbreviation,
                'name': s.name
            }
            
        data['base_products_json'] = json.dumps(bp_data)
        data['supplies_json'] = json.dumps(supply_data)
        
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        bom_formset = context['bom_formset']
        if form.is_valid() and bom_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                bom_formset.instance = self.object
                bom_formset.save()
                
                # Handle multiple files
                files = self.request.FILES.getlist('more_files')
                if files:
                    from .models import ProductImage
                    for f in files:
                        ProductImage.objects.create(product=self.object, image=f)

            return super(CreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class FinalProductUpdateView(SuccessMessageMixin, UpdateView):
    model = FinalProduct
    form_class = FinalProductForm
    template_name = 'production/finalproduct_form.html'
    success_url = reverse_lazy('finalproduct-list')
    success_message = "Producto Final actualizado exitosamente."

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['bom_formset'] = BOMFormSet(self.request.POST, instance=self.object)
        else:
            data['bom_formset'] = BOMFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        bom_formset = context['bom_formset']
        if form.is_valid() and bom_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                bom_formset.save()
                
                # Handle multiple files
                files = self.request.FILES.getlist('more_files')
                if files:
                    from .models import ProductImage
                    for f in files:
                        ProductImage.objects.create(product=self.object, image=f)

            return super(UpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class FinalProductDetailView(DetailView):
    model = FinalProduct
    template_name = 'production/finalproduct_detail.html'
    context_object_name = 'product'

class FinalProductDeleteView(DeleteView):
    model = FinalProduct
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('finalproduct-list')
