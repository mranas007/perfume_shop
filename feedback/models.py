from django.db import models
from accounts.models import User
from catalog.models import Product



class Customer_feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    add_to_list = models.BooleanField(default=False)
    top_feedback = models.BooleanField(default=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']