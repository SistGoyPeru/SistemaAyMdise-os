import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
django.setup()

from djmoney.money import Money
from inventory.models import UnitOfMeasure, Supply, BaseProduct, Category
from production.models import FinalProduct, BillOfMaterial
from sales.models import Customer, Order, OrderItem

def run():
    print("Iniciando carga de datos de demostración...")

    # --- 1. Unidades de Medida ---
    print("Creando Unidades...")
    units = {
        'und': 'Unidad',
        'ml': 'Mililitros',
        'kg': 'Kilogramos',
        'm': 'Metros',
        'roll': 'Rollo'
    }
    unit_objs = {}
    for abbr, name in units.items():
        u, _ = UnitOfMeasure.objects.get_or_create(abbreviation=abbr, defaults={'name': name})
        unit_objs[abbr] = u

    # --- 2. Categorías ---
    print("Creando Categorías...")
    categories = ['Maquinaria', 'Tintas', 'Papelería', 'Textiles', 'Cerámica', 'Otros']
    cat_objs = {}
    for c in categories:
        cat, _ = Category.objects.get_or_create(name=c)
        cat_objs[c] = cat

    # --- 3. Insumos (Supplies) ---
    print("Creando Insumos...")
    supplies_data = [
        # Maquinaria
        {'name': 'Impresora Epson L1800', 'cat': 'Maquinaria', 'unit': 'und', 'stock': 2, 'min': 1, 'cost': 500.00},
        {'name': 'Plancha Térmica 38x38', 'cat': 'Maquinaria', 'unit': 'und', 'stock': 1, 'min': 1, 'cost': 250.00},
        # Tintas
        {'name': 'Tinta Sublimación Cyan', 'cat': 'Tintas', 'unit': 'ml', 'stock': 500, 'min': 100, 'cost': 0.08},
        {'name': 'Tinta Sublimación Magenta', 'cat': 'Tintas', 'unit': 'ml', 'stock': 450, 'min': 100, 'cost': 0.08},
        {'name': 'Tinta Sublimación Yellow', 'cat': 'Tintas', 'unit': 'ml', 'stock': 600, 'min': 100, 'cost': 0.08},
        {'name': 'Tinta Sublimación Black', 'cat': 'Tintas', 'unit': 'ml', 'stock': 300, 'min': 100, 'cost': 0.08},
        # Papelería
        {'name': 'Papel Sublimación A4', 'cat': 'Papelería', 'unit': 'und', 'stock': 500, 'min': 50, 'cost': 0.05},
        {'name': 'Papel Transfer', 'cat': 'Papelería', 'unit': 'und', 'stock': 200, 'min': 20, 'cost': 0.10},
        # Otros
        {'name': 'Cinta Térmica', 'cat': 'Otros', 'unit': 'und', 'stock': 10, 'min': 2, 'cost': 2.00},
    ]

    supply_objs = {}
    for d in supplies_data:
        s, _ = Supply.objects.get_or_create(
            name=d['name'],
            defaults={
                'category': cat_objs[d['cat']],
                'unit': unit_objs[d['unit']],
                'stock': d['stock'],
                'min_stock': d['min'],
                'cost_per_unit': Money(d['cost'], 'USD')
            }
        )
        supply_objs[d['name']] = s

    # --- 4. Productos Base ---
    print("Creando Productos Base...")
    base_data = [
        {'name': 'Taza Blanca 11oz', 'stock': 100, 'min': 12, 'cost': 1.20},
        {'name': 'Taza Mágica 11oz', 'stock': 36, 'min': 5, 'cost': 2.50},
        {'name': 'Polo Algodón Blanco S', 'stock': 50, 'min': 10, 'cost': 3.50},
        {'name': 'Polo Algodón Blanco M', 'stock': 40, 'min': 10, 'cost': 3.50},
        {'name': 'Polo Algodón Blanco L', 'stock': 60, 'min': 10, 'cost': 3.50},
        {'name': 'Gorra Camionera', 'stock': 25, 'min': 5, 'cost': 1.80},
    ]

    base_objs = {}
    for d in base_data:
        b, _ = BaseProduct.objects.get_or_create(
            name=d['name'],
            defaults={
                'stock': d['stock'],
                'min_stock': d['min'],
                'cost': Money(d['cost'], 'USD'),
                'description': 'Producto listo para estampar'
            }
        )
        base_objs[d['name']] = b

    # --- 5. Productos Finales (Recetas) ---
    print("Creando Productos Finales y Recetas...")
    final_data = [
        {'name': 'Taza Personalizada (Foto)', 'base': 'Taza Blanca 11oz', 'price': 15.00, 'supplies': [('Tinta Sublimación Black', 5), ('Papel Sublimación A4', 1)]}, # 5ml tinta, 1 hoja
        {'name': 'Polo Logo Empresa (Pecho)', 'base': 'Polo Algodón Blanco M', 'price': 25.00, 'supplies': [('Tinta Sublimación Cyan', 2), ('Papel Transfer', 1)]},
    ]

    final_objs = []
    for d in final_data:
        fp, created = FinalProduct.objects.get_or_create(
            name=d['name'],
            defaults={
                'base_product': base_objs[d['base']],
                'sale_price': Money(d['price'], 'USD')
            }
        )
        final_objs.append(fp)
        
        if created:
            for supply_name, qty in d['supplies']:
                BillOfMaterial.objects.create(
                    final_product=fp,
                    supply=supply_objs[supply_name],
                    quantity=qty
                )

    # --- 6. Clientes ---
    print("Creando Clientes...")
    clients = [
        {'name': 'Juan Pérez', 'email': 'juan@gmail.com', 'phone': '999888777'},
        {'name': 'Empresa ABC S.A.C.', 'email': 'contacto@abc.com', 'phone': '01-4445555'},
        {'name': 'María López', 'email': 'maria@hotmail.com', 'phone': '987654321'},
    ]
    
    client_objs = []
    for c in clients:
        cli, _ = Customer.objects.get_or_create(
            email=c['email'],
            defaults={'name': c['name'], 'phone': c['phone']}
        )
        client_objs.append(cli)

    # --- 7. Pedidos (Ventas) ---
    print("Creando Pedidos de Ejemplo...")
    
    # Pedido 1: Pendiente
    o1 = Order.objects.create(customer=client_objs[0], status='PENDING')
    OrderItem.objects.create(order=o1, product=final_objs[0], quantity=2, price=final_objs[0].sale_price) # 2 Tazas
    o1.calculate_total()
    
    # Pedido 2: En Prensa (Ya descontó stock en teoría si lo hacemos manual, pero create directo via script no dispara signal igual que formulario a veces, pero signal save si)
    o2 = Order.objects.create(customer=client_objs[1], status='IN_PRESS')
    # OJO: Al crear items manualmente aqui, el signal post_save de OrderItem podría dispararse si está configurado
    item = OrderItem.objects.create(order=o2, product=final_objs[1], quantity=10, price=final_objs[1].sale_price) # 10 Polos
    # El signal para IN_PRESS revisa cambios de status. Aqui status ya es IN_PRESS al crear.
    # Para simular flujo:
    o2.status = 'PENDING'
    o2.save() # Reset
    o2.status = 'IN_PRESS'
    o2.save() # Trigger descuento
    o2.calculate_total()
    
    # Pedido 3: Finalizado
    o3 = Order.objects.create(customer=client_objs[2], status='DELIVERED')
    OrderItem.objects.create(order=o3, product=final_objs[0], quantity=1, price=final_objs[0].sale_price)
    o3.created_at = timezone.now() - timedelta(days=5) # Pedido antiguo
    o3.save()
    o3.calculate_total()

    print("\n¡Datos de demostración cargados exitosamente!")
    print("Revisa el Dashboard y las listas de Inventario/Ventas.")

if __name__ == '__main__':
    run()
