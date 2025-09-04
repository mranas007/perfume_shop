from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
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
    """Update cart item quantity"""
    if request.method == 'POST':
        print(f"Cart update called for item {item_id}")  # Debug print
        print(f"POST data: {request.POST}")  # Debug print

        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        print(f"Current quantity: {cart_item.quantity}, New quantity: {quantity}")  # Debug print

        if quantity > 0:
            cart_item.update_quantity(quantity)
            messages.success(request, f"Quantity updated to {quantity}.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")

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