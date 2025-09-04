from django.db import models
from django.conf import settings
from django.utils import timezone

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at time of adding to cart")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']  # Prevent duplicate cart items
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Set price from product if not set
        if not self.price and self.product.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def update_quantity(self, new_quantity):
        """Update quantity and save"""
        if new_quantity > 0:
            self.quantity = new_quantity
            self.save()
        else:
            self.delete()  # Remove if quantity is 0 or negative