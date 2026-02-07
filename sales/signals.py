from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Order, OrderItem

@receiver(pre_save, sender=Order)
def check_order_status_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            instance._old_status = old_order.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

def deduct_stock_for_item(item):
    """Auxiliary function to deduct stock for a single OrderItem."""
    final_prod = item.product
    quantity_ordered = item.quantity

    # 1. Descontar Producto Base
    base_prod = final_prod.base_product
    if base_prod.stock >= quantity_ordered:
        base_prod.stock -= quantity_ordered
        base_prod.save()
    else:
        # If stock is insufficient, we raise an error to rollback transaction
        raise ValidationError(f"Stock insuficiente para el producto base: {base_prod.name}. Stock actual: {base_prod.stock}, Requerido: {quantity_ordered}")

    # 2. Descontar Insumos (BOM)
    for bom in final_prod.billofmaterial_set.all():
        supply = bom.supply
        total_supply_needed = bom.quantity * quantity_ordered
        
        # Supply.stock is DecimalField
        if supply.stock >= total_supply_needed:
            supply.stock -= total_supply_needed
            supply.save()
        else:
             raise ValidationError(f"Stock insuficiente para insumo: {supply.name}. Stock actual: {supply.stock}, Requerido: {total_supply_needed}")


@receiver(post_save, sender=Order)
def deduct_stock_on_order_change(sender, instance, created, **kwargs):
    # Process if status changed to 'IN_PRESS'
    if getattr(instance, '_old_status', None) != 'IN_PRESS' and instance.status == 'IN_PRESS':
        
        # When creating a new order with 'IN_PRESS', items might not be saved yet if using CreateView standard flow.
        # But if updating, items exist.
        if instance.items.exists():
            for item in instance.items.all():
                deduct_stock_for_item(item)

@receiver(post_save, sender=OrderItem)
def deduct_stock_on_item_save(sender, instance, created, **kwargs):
    # If the order is ALREADY in 'IN_PRESS' state, adding an item should deduct stock immediately.
    # This covers the "Create with IN_PRESS" scenario where items are saved AFTER order.
    if instance.order.status == 'IN_PRESS':
        # We check if this item was just created or if quantity increased?
        # For simplicity, if created, deduct full amount. 
        # If updated, it's harder (need old quantity). Assuming simple create for now.
        if created:
            deduct_stock_for_item(instance)
