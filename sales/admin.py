from django.contrib import admin
from .models import Customer, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at', 'design_link')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'id')
    inlines = [OrderItemInline]
    actions = ['mark_in_press', 'mark_finished']

    def design_link(self, obj):
        if obj.design_url:
            return f'<a href="{obj.design_url}" target="_blank">Ver Diseño</a>'
        return "-"
    design_link.allow_tags = True
    design_link.short_description = "Diseño"

    def mark_in_press(self, request, queryset):
        # This will trigger the signal if status changes
        updated = queryset.update(status='IN_PRESS')
        # Note: queryset.update does NOT send signals.
        # So we must iterate and save() to trigger the stock deduction signal.
        # But for bulk actions, this is slow. 
        # However, the requirement is to use signals. 
        # Let's override the action to use save().
        for order in queryset:
            if order.status != 'IN_PRESS':
                order.status = 'IN_PRESS'
                order.save()
        self.message_user(request, f"{updated} pedidos marcados como 'En Prensa'.")
    mark_in_press.short_description = "Marcar como En Prensa"

    def mark_finished(self, request, queryset):
        queryset.update(status='FINISHED')
    mark_finished.short_description = "Marcar como Terminado"
