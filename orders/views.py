from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Order
from catalog.models import Product

# Create your views here.
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Enhance orders with product details
    for order in orders:
        order_items = []
        total_amount = 0
        if order.cart_details:
            for product_id, quantity in order.cart_details.items():
                try:
                    product = Product.objects.get(id=product_id)
                    item_total = product.price * quantity if product.price else 0
                    total_amount += item_total
                    order_items.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price,
                        'total': item_total
                    })
                except Product.DoesNotExist:
                    continue
        order.items = order_items
        order.total_amount = total_amount

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
        'paginator': paginator,
        'page_obj': page_obj
    }
    return render(request, 'orders/order_list.html', context)