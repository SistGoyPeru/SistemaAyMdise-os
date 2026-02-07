from django import forms
from django.forms import inlineformset_factory
from .models import FinalProduct, BillOfMaterial

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class FinalProductForm(forms.ModelForm):
    more_files = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Archivos Adicionales (Selecciona varios con Ctrl)",
        required=False
    )

    class Meta:
        model = FinalProduct
        fields = ['name', 'base_product', 'supplies_cost', 'other_cost', 'sale_price', 'design_file'] 
        widgets = {
            'design_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

BOMFormSet = inlineformset_factory(
    FinalProduct, 
    BillOfMaterial, 
    fields=['supply', 'quantity'],
    extra=0,
    can_delete=True
)
