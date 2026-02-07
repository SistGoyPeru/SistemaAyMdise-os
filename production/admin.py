from django.contrib import admin
from .models import FinalProduct, BillOfMaterial

class BOMInline(admin.TabularInline):
    model = BillOfMaterial
    extra = 1
    autocomplete_fields = ['supply']

@admin.register(FinalProduct)
class FinalProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_product', 'get_cost', 'sale_price', 'get_margin')
    search_fields = ('name',)
    inlines = [BOMInline]

    def get_cost(self, obj):
        return obj.calculate_production_cost()
    get_cost.short_description = "Costo Producción"

    def get_margin(self, obj):
        return obj.calculate_profit_margin()
    get_margin.short_description = "Margen Ganancia"
