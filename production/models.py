from django.db import models
from inventory.models import BaseProduct, Supply
from djmoney.models.fields import MoneyField

class FinalProduct(models.Model):
    """
    Producto Final listo para la venta (ej. Taza Spiderman).
    Se compone de un Producto Base (Taza) + Insumos (Tinta/Papel) + Diseño.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    base_product = models.ForeignKey(BaseProduct, on_delete=models.PROTECT, verbose_name="Producto Base")
    sale_price = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', verbose_name="Precio de Venta")
    
    # Manual Costs (Simplified)
    supplies_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', default=0, verbose_name="Costo Insumos (Manual)")
    other_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', default=0, verbose_name="Otros Costos (Mano de obra, etc)")
    
    supplies = models.ManyToManyField(Supply, through='BillOfMaterial', verbose_name="Insumos Requeridos", blank=True)
    design_file = models.FileField(upload_to='designs/', blank=True, null=True, verbose_name="Archivo de Diseño Principal")

    def __str__(self):
        return self.name

    def calculate_production_cost(self):
        # Costo Base
        total = self.base_product.cost.amount
        
        # Costos Manuales
        total += self.supplies_cost.amount
        total += self.other_cost.amount
        
        # Costo Insumos (BOM) - Optional
        for bom in self.billofmaterial_set.all():
            total += (bom.supply.cost_per_unit.amount * bom.quantity)
            
        return total

    def calculate_profit_margin(self):
        cost = self.calculate_production_cost()
        price = self.sale_price.amount
        if price > 0:
            margin = ((price - cost) / price) * 100
            return f"{margin:.1f}%"
        return "0%"

class ProductImage(models.Model):
    product = models.ForeignKey(FinalProduct, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='designs/extras/', verbose_name="Archivo Adicional")

    def __str__(self):
        return f"Imagen para {self.product.name}"

class BillOfMaterial(models.Model):
    """
    Receta: Cantidad de insumo para 1 unidad de producto final.
    """
    final_product = models.ForeignKey(FinalProduct, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=4, default=1)

    def __str__(self):
        return f"{self.supply.name} ({self.quantity}) -> {self.final_product.name}"
