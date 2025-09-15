from django.contrib import admin
from . import models

admin.site.site_header = "Administration"
admin.site.index_title = "Adnan Perfume Administration"

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock', 'top_listed']
    list_filter = ['category', 'brand', 'top_listed', 'created_at']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'top_listed']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'product', 'rating', 'active', 'on_board', 'created_at']
    list_filter = ['rating', 'active', 'on_board', 'created_at']
    search_fields = ['user_name', 'product__name', 'comment']
    list_editable = ['active', 'on_board']
    readonly_fields = ['created_at']
