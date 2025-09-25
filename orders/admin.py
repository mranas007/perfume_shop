from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order
from catalog.models import Product

class OrderItemInline(admin.TabularInline):
    model = Order
    readonly_fields = ('product_info', 'quantity', 'price', 'item_total')
    can_delete = False
    max_num = 0
    extra = 0

    def product_info(self, obj):
        if obj.cart_details:
            product_info = []
            for product_id, quantity in obj.cart_details.items():
                try:
                    product = Product.objects.get(id=product_id)
                    product_info.append(f"{product.name} ({product.brand or 'No Brand'})")
                except Product.DoesNotExist:
                    product_info.append(f"Product {product_id} (Not Found)")
            return format_html('<br>'.join(product_info))
        return "No items"
    product_info.short_description = "Products"

    def price(self, obj):
        if obj.cart_details:
            prices = []
            for product_id, quantity in obj.cart_details.items():
                try:
                    product = Product.objects.get(id=product_id)
                    prices.append(f"PKR {product.price or 0}")
                except Product.DoesNotExist:
                    prices.append("N/A")
            return format_html('<br>'.join(prices))
        return "N/A"

    def item_total(self, obj):
        if obj.cart_details:
            totals = []
            for product_id, quantity in obj.cart_details.items():
                try:
                    product = Product.objects.get(id=product_id)
                    total = (product.price or 0) * quantity
                    totals.append(f"PKR {total}")
                except Product.DoesNotExist:
                    totals.append("N/A")
            return format_html('<br>'.join(totals))
        return "N/A"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name', 'customer_phone', 'status', 'created_at', 'total_amount', 'item_count', 'order_products')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('id', 'customer_name', 'customer_phone', 'user__name', 'user__email', 'customer_address')
    readonly_fields = ('id', 'created_at', 'user', 'customer_name', 'customer_phone', 'customer_address', 'cart_details', 'order_items_display')
    ordering = ('-created_at',)
    list_editable = ('status',)
    list_per_page = 25

    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'status', 'created_at')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone', 'customer_address')
        }),
        ('Order Items', {
            'fields': ('order_items_display', 'cart_details'),
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_delivered', 'mark_as_cancelled']

    def status_badge(self, obj):
        status_colors = {
            'pending': 'yellow',
            'confirmed': 'blue',
            'processing': 'orange',
            'delivered': 'green',
            'cancelled': 'red'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{0}-100 text-{0}-800">'
            '{1}'
            '</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def total_amount(self, obj):
        total = 0
        if obj.cart_details:
            for product_id, quantity in obj.cart_details.items():
                try:
                    product = Product.objects.get(id=product_id)
                    total += (product.price or 0) * quantity
                except Product.DoesNotExist:
                    continue
        return format_html('<strong>PKR {}</strong>', int(total))
    total_amount.short_description = "Total Amount"

    def item_count(self, obj):
        if obj.cart_details:
            return sum(obj.cart_details.values())
        return 0
    item_count.short_description = "Items"

    def order_products(self, obj):
        if not obj.cart_details:
            return "No products"

        product_names = []
        for product_id, quantity in list(obj.cart_details.items())[:3]:  # Show first 3 products
            try:
                product = Product.objects.get(id=product_id)
                product_names.append(f"{product.name} (x{quantity})")
            except Product.DoesNotExist:
                product_names.append(f"Product {product_id} (x{quantity})")

        products_text = ", ".join(product_names)

        # If there are more than 3 products, add a count
        total_items = len(obj.cart_details)
        if total_items > 3:
            products_text += f" +{total_items - 3} more"

        return products_text
    order_products.short_description = "Products"

    def order_items_display(self, obj):
        if not obj.cart_details:
            return "No items in this order"

        items_html = []
        total_amount = 0

        for product_id, quantity in obj.cart_details.items():
            try:
                product = Product.objects.get(id=product_id)
                item_total = (product.price or 0) * quantity
                total_amount += item_total

                items_html.append(format_html(
                    '<div class="mb-2 p-2 bg-gray-50 rounded">'
                    '<strong>{}</strong> ({})<br>'
                    'Quantity: {} × PKR {} = <strong>PKR {}</strong>'
                    '</div>',
                    product.name, product.brand or 'No Brand',
                    quantity, int(product.price or 0), int(item_total)
                ))
            except Product.DoesNotExist:
                items_html.append(format_html(
                    '<div class="mb-2 p-2 bg-red-50 rounded text-red-700">'
                    'Product {} not found (Quantity: {})'
                    '</div>',
                    product_id, quantity
                ))

        items_html.append(format_html(
            '<div class="mt-3 p-3 bg-blue-50 rounded font-bold text-blue-800">'
            'Total Order Value: PKR {}'
            '</div>',
            int(total_amount)
        ))

        return format_html(''.join(items_html))
    order_items_display.short_description = "Order Items Details"

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')
    mark_as_processing.short_description = "Mark selected orders as processing"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"
