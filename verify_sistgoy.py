
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
django.setup()

from inventory.models import UnitOfMeasure, Supply, BaseProduct
from production.models import FinalProduct, BillOfMaterial
from sales.models import Customer, Order, OrderItem
from djmoney.money import Money

def run_verification():
    print("Iniciando Verificación del Sistema SistGoy ERP...")

    # 1. Crear Datos de Inventario
    print("\n[INVENTARIO] Creando datos...")
    # Limpiar datos previos
    UnitOfMeasure.objects.all().delete()
    Supply.objects.all().delete()
    BaseProduct.objects.all().delete()
    FinalProduct.objects.all().delete()
    Customer.objects.all().delete()
    Order.objects.all().delete()

    unit_ml = UnitOfMeasure.objects.create(name="Mililitros", abbreviation="ml")
    unit_und = UnitOfMeasure.objects.create(name="Unidad", abbreviation="und")

    supply_ink = Supply.objects.create(
        name="Tinta Sublimación",
        unit=unit_ml,
        stock=1000,  # 1 Litro
        cost_per_unit=Money(0.05, 'USD') # $0.05 por ml
    )
    
    base_mug = BaseProduct.objects.create(
        name="Taza Blanca 11oz",
        stock=100,
        cost=Money(1.50, 'USD')
    )

    print(f"Creado Insumo: {supply_ink} (Stock: {supply_ink.stock})")
    print(f"Creado Producto Base: {base_mug} (Stock: {base_mug.stock})")

    # 2. Crear Producto Final y BOM
    print("\n[PRODUCCIÓN] Creando Producto Final y Receta...")
    final_mug = FinalProduct.objects.create(
        name="Taza Personalizada SistGoy",
        base_product=base_mug,
        sale_price=Money(10.00, 'USD')
    )

    # Receta: 1 Taza consume 10ml de tinta
    BillOfMaterial.objects.create(
        final_product=final_mug,
        supply=supply_ink,
        quantity=10
    )

    print(f"Producto Final: {final_mug}")
    print(f"Costo de Producción: {final_mug.calculate_production_cost()}")
    print(f"Margen de Ganancia: {final_mug.calculate_profit_margin()}")

    assert final_mug.calculate_production_cost().amount == 1.50 + (10 * 0.05) # 1.50 + 0.50 = 2.00
    print("CHECK: Cálculo de costo correcto.")

    # 3. Crear Venta
    print("\n[VENTAS] Creando Pedido...")
    customer = Customer.objects.create(name="Juan Perez", email="juan@example.com")
    
    order = Order.objects.create(customer=customer)
    OrderItem.objects.create(order=order, product=final_mug, quantity=5, price=final_mug.sale_price)
    order.calculate_total()
    
    print(f"Pedido Creado: {order} - Total: {order.total_amount}")
    print(f"Estado Actual: {order.get_status_display()}")

    # Verificar stock antes del cambio
    print(f"Stock Antes -> Taza Base: {BaseProduct.objects.get(pk=base_mug.pk).stock}, Tinta: {Supply.objects.get(pk=supply_ink.pk).stock}")

    # 4. Cambiar estado a 'En Prensa' y verificar descuento
    print("\n[LÓGICA] Cambiando estado a 'En Prensa'...")
    order.status = 'IN_PRESS'
    order.save()

    # Recargar objetos de la DB
    base_mug.refresh_from_db()
    supply_ink.refresh_from_db()

    print(f"Stock Después -> Taza Base: {base_mug.stock}, Tinta: {supply_ink.stock}")

    # Verificaciones
    assert base_mug.stock == 100 - 5 # 95
    assert supply_ink.stock == 1000 - (5 * 10) # 1000 - 50 = 950

    print("CHECK: Descuento de stock correcto.")
    print("\nVERIFICACIÓN COMPLETADA EXITOSAMENTE.")

if __name__ == "__main__":
    run_verification()
