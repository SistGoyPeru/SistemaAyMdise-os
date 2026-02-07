from django.db import models
from djmoney.models.fields import MoneyField

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    abbreviation = models.CharField(max_length=10, unique=True, verbose_name="Abreviatura")

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
    
    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

class BaseProduct(models.Model):
    """
    Productos sin estampar (polos en blanco, tazas en blanco, etc.)
    """
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    cost = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN')
    image = models.ImageField(upload_to='base_products/', blank=True, null=True, verbose_name="Imagen del Producto Base (Mockup)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto Base"
        verbose_name_plural = "Productos Base"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Supply(models.Model):
    """
    Insumos como tinta, papel, cinta, y ahora Maquinaria (Impresoras, Planchas).
    """
    name = models.CharField(max_length=100, verbose_name="Nombre")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría")
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, verbose_name="Unidad de Medida")
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock Actual")
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock Mínimo")
    cost_per_unit = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', verbose_name="Costo por Unidad")

    def __str__(self):
        return f"{self.name} ({self.stock} {self.unit.abbreviation})"

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
