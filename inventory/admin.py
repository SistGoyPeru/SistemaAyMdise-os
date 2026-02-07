from django.contrib import admin
from .models import UnitOfMeasure, BaseProduct, Supply

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')

@admin.register(BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'min_stock', 'cost')
    search_fields = ('name',)
    list_filter = ('stock', 'min_stock')

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'unit', 'min_stock', 'cost_per_unit')
    search_fields = ('name',)
    list_filter = ('unit',)
