from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'design_url']

OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem, 
    fields=['product', 'quantity', 'price'],
    extra=1,
    can_delete=True
)
