from django.contrib import admin
from .models import Product, Category, Review

admin.site.site_header = "Administration"
admin.site.index_title = "Adnan Perfume Administration"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'top_listed', 'price', 'stock', 'original_price')
    list_editable = ('top_listed','stock')
    list_per_page = 20
    search_fields = ('name', 'brand', 'category__name')
    prepopulated_fields = {'slug': ('name',)}

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name','product__name', 'rating', 'active', 'on_board')
    list_editable = ('active', 'on_board')
    list_per_page = 20
    search_fields = ('product__name', 'user_name')


admin.site.register(Review, ReviewAdmin)
