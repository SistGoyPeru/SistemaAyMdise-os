import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistgoy_erp.settings')
django.setup()

from inventory.models import Supply, BaseProduct
from production.models import FinalProduct, BillOfMaterial
from sales.models import Order, OrderItem, Customer

def run():
    print("WARNING: This will delete all business data (Orders, Products, Inventory).")
    confirm = input("Are you sure? Type 'yes' to proceed: ")
    if confirm != 'yes':
        print("Operation cancelled.")
        return

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

    print("\n---------------------------------------------------")
    print("DATA CLEARED SUCCESSFULLY.")
    print("Categories and Units of Measure were preserved.")
    print("You can now start entering your real data.")
    print("---------------------------------------------------")

if __name__ == '__main__':
    run()
