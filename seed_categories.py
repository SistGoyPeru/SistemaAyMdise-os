import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
django.setup()

from inventory.models import Category

names = ['Maquinaria', 'Consumibles', 'Repuestos', 'Otros']
print("Creando categorías por defecto...")

for n in names:
    cat, created = Category.objects.get_or_create(name=n)
    if created:
        print(f" - Creada: {n}")
    else:
        print(f" - Ya existe: {n}")

print("Listo!")
