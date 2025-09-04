from .models import CartItem

def cart_count(request):
    """Context processor to add cart information to all templates"""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        cart_count = cart_items.count()
        cart_total = sum(item.total_price for item in cart_items)
        # Create a set of product IDs in cart for quick lookup
        cart_product_ids = set(item.product_id for item in cart_items)
    else:
        cart_items = []
        cart_count = 0
        cart_total = 0
        cart_product_ids = set()

    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
        'cart_product_ids': cart_product_ids,
    }