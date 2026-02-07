from django.db import models
from production.models import FinalProduct
from djmoney.models.fields import MoneyField

class Customer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre Cliente")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PRESS', 'En Prensa'),
        ('FINISHED', 'Terminado'),
        ('DELIVERED', 'Entregado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Cliente")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    total_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', default=0, verbose_name="Monto Total")
    design_url = models.URLField(max_length=500, blank=True, verbose_name="URL Diseño (Drive/Cloudinary)")

    def calculate_total(self):
        total = 0
        for item in self.items.all():
            total += item.price * item.quantity
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer.name} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(FinalProduct, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='PEN', verbose_name="Precio Unitario")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.price * self.quantity
