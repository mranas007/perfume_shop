from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from catalog.models import Product
from orders.models import Order
from .models import CartItem

@login_required
def cart_details(request):
    """Display user's cart items"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_total = sum(item.total_price for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'item_count': item_count,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)

    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'price': product.price or 0}
    )

    if not created:
        # Item exists, increase quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Increased {product.name} quantity in cart.")
    else:
        messages.success(request, f"{product.name} added to cart.")

    # Redirect back to previous page or product detail
    next_url = request.GET.get('next', 'cart:cart_detail')
    return redirect(next_url)

@login_required
def cart_update(request, item_id):
    """Update cart item quantity - supports both AJAX and regular form submissions"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        # Validate stock
        if quantity > cart_item.product.stock:
            error_msg = f"Only {cart_item.product.stock} items available in stock."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
            messages.error(request, error_msg)
            return redirect('cart:cart_detail')

        if quantity > 0:
            cart_item.update_quantity(quantity)
            success_msg = f"Quantity updated to {quantity}."

            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON response for AJAX
                return JsonResponse({
                    'success': True,
                    'message': success_msg,
                    'item_id': item_id,
                    'quantity': quantity,
                    'item_total': float(cart_item.total_price),
                    'cart_total': float(sum(item.total_price for item in CartItem.objects.filter(user=request.user))),
                    'cart_count': CartItem.objects.filter(user=request.user).count()
                })
            else:
                # Regular form submission - redirect
                messages.success(request, success_msg)
        else:
            cart_item.delete()
            success_msg = "Item removed from cart."

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_msg,
                    'item_removed': True,
                    'cart_total': float(sum(item.total_price for item in CartItem.objects.filter(user=request.user))),
                    'cart_count': CartItem.objects.filter(user=request.user).count()
                })
            else:
                messages.success(request, success_msg)

    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.success(request, f"{product_name} removed from cart.")
    return redirect('cart:cart_detail')

@login_required
def cart_clear(request):
    """Clear all items from cart"""
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Cart cleared successfully.")
    return redirect('cart:cart_detail')

@login_required
def checkout(request):
    """Display checkout form"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    cart_total = sum(item.total_price for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)

    # Pre-fill form with user data
    initial_data = {
        'customer_name': request.user.name,
        'customer_phone': getattr(request.user, 'phone', ''),
    }

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'item_count': item_count,
        'initial_data': initial_data,
    }
    return render(request, 'cart/checkout.html', context)

@login_required
def place_order(request):
    """Process order placement"""
    if request.method != 'POST':
        return redirect('cart:checkout')

    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    # Get form data
    customer_name = request.POST.get('customer_name', '').strip()
    customer_phone = request.POST.get('customer_phone', '').strip()
    customer_address = request.POST.get('customer_address', '').strip()

    # Validate required fields
    if not customer_name or not customer_phone or not customer_address:
        messages.error(request, "Please fill in all required fields.")
        return redirect('cart:checkout')

    # Create cart details dictionary
    cart_details = {}
    total_amount = 0

    for item in cart_items:
        cart_details[str(item.product.id)] = item.quantity
        total_amount += item.total_price

    # Create the order
    order = Order.objects.create(
        user=request.user,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_address=customer_address,
        cart_details=cart_details,
        status='pending'
    )

    # Clear the cart
    cart_items.delete()

    messages.success(request, f"Order #{order.id} placed successfully! We will contact you soon for payment and delivery.")

    return redirect('orders:order_confirmation', order_id=order.id)