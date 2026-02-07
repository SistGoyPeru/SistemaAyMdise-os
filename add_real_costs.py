import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
django.setup()

from djmoney.money import Money
from inventory.models import UnitOfMeasure, Supply, BaseProduct, Category

def run():
    print("Adding real-world items based on user request (Taza 11oz)...")

    # 1. Categories
    cat_indirect, _ = Category.objects.get_or_create(name='Costos Indirectos')
    cat_packaging, _ = Category.objects.get_or_create(name='Empaques')
    cat_services, _ = Category.objects.get_or_create(name='Servicios de Impresión') # Simplified printing

    # 2. Units
    u_und, _ = UnitOfMeasure.objects.get_or_create(abbreviation='und', defaults={'name': 'Unidad'})
    u_srv, _ = UnitOfMeasure.objects.get_or_create(abbreviation='srv', defaults={'name': 'Servicio'})

    # 3. Base Product: Taza Blanca 11oz AAA
    # Avg cost S/ 4.20
    taza, created = BaseProduct.objects.get_or_create(
        name='Taza Blanca 11oz AAA',
        defaults={
            'description': 'Taza de alta calidad para sublimación.',
            'category': Category.objects.get(name='Cerámica') if Category.objects.filter(name='Cerámica').exists() else None,
            'stock': 36,
            'cost': Money(4.20, 'PEN') # Using configured currency, user treats as local currency
        }
    )
    if not created:
        taza.cost = Money(4.20, 'PEN')
        taza.save()
    print(f"Updated/Created: {taza.name}")

    # 4. Supplies (Insumos)
    
    # 4.1 Impresión (Tinta + Papel) - Simplified
    # Cost S/ 0.50
    print_srv, _ = Supply.objects.get_or_create(
        name='Impresión Sublimación (Hoja+Tinta)',
        defaults={
            'category': cat_services,
            'unit': u_srv,
            'stock': 9999, # Infinite service
            'min_stock': 0,
            'cost_per_unit': Money(0.50, 'PEN')
        }
    )
    
    # 4.2 Cinta Térmica
    # Cost S/ 0.10 per use (approx)
    cat_others = Category.objects.filter(name='Otros').first()
    tape, _ = Supply.objects.get_or_create(
        name='Cinta Térmica (Uso por Taza)',
        defaults={
            'category': cat_others,
            'unit': u_und,
            'stock': 1000,
            'min_stock': 100,
            'cost_per_unit': Money(0.10, 'PEN')
        }
    )
    
    # 4.3 Luz y Desgaste
    # Cost S/ 0.20
    overhead, _ = Supply.objects.get_or_create(
        name='Costo Op. (Luz + Desgaste Prensa)',
        defaults={
            'category': cat_indirect,
            'unit': u_srv,
            'stock': 9999,
            'min_stock': 0,
            'cost_per_unit': Money(0.20, 'PEN')
        }
    )

    # 4.4 Caja Individual
    # Cost S/ 1.00
    box, _ = Supply.objects.get_or_create(
        name='Caja Cartón Individual Taza',
        defaults={
            'category': cat_packaging,
            'unit': u_und,
            'stock': 100,
            'min_stock': 10,
            'cost_per_unit': Money(1.00, 'PEN')
        }
    )

    print("Items added successfully!")

if __name__ == '__main__':
    run()
