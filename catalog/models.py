from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    on_board = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user_name} for {self.product.name}"   

class Product(models.Model):
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/')
    top_listed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.brand or 'No Brand'} | {self.category.name if self.category else 'No Category'}"
