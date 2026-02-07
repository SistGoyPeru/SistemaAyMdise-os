import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
try:
    django.setup()
except Exception as e:
    pass

from inventory.models import Supply, BaseProduct
from production.models import FinalProduct, BillOfMaterial
from sales.models import Order, OrderItem, Customer

def run():
    print("Deleting Orders and Items...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    
    print("Deleting Production Data...")
    BillOfMaterial.objects.all().delete()
    FinalProduct.objects.all().delete()
    
    print("Deleting Inventory (Supplies & Base Products)...")
    Supply.objects.all().delete()
    BaseProduct.objects.all().delete()
    
    print("Deleting Customers...")
    Customer.objects.all().delete()

    print("DATA CLEARED SUCCESSFULLY.")

if __name__ == '__main__':
    run()
