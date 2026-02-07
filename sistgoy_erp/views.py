from django.shortcuts import render
from django.db import models
from django.utils import timezone
from sales.models import Order
from inventory.models import Supply, BaseProduct

def dashboard(request):
    # Metrics
    pending_orders_count = Order.objects.filter(status='PENDING').count()
    in_press_count = Order.objects.filter(status='IN_PRESS').count()
    
    # Low Stock (Naive implementation: verify if stock <= min_stock)
    low_stock_supplies = Supply.objects.filter(stock__lte=models.F('min_stock')).count()
    low_stock_products = BaseProduct.objects.filter(stock__lte=models.F('min_stock')).count()
    low_stock_count = low_stock_supplies + low_stock_products

    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    # Monthly Sales
    now = timezone.now()
    monthly_sales = Order.objects.filter(
        created_at__month=now.month, 
        created_at__year=now.year
    ).exclude(status='PENDING').aggregate(total=models.Sum('total_amount'))['total'] or 0

    context = {
        'today': timezone.now(),
        'pending_orders_count': pending_orders_count,
        'in_press_count': in_press_count,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
        'monthly_sales': monthly_sales,
    }
    return render(request, 'dashboard.html', context)
