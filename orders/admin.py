from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name', 'customer_phone', 'status', 'created_at', 'total_amount')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('id', 'customer_name', 'customer_phone', 'user__name', 'user__email')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)

    def total_amount(self, obj):
        if hasattr(obj, 'total_amount'):
            return f"PKR {obj.total_amount}"
        return "N/A"
    total_amount.short_description = "Total Amount"
