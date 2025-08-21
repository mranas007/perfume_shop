from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404




def catalog_page(request):
    category_slug = request.GET.get('category_slug', '')
    if category_slug:
        products = Product.objects.filter(category__slug__icontains=category_slug)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()[:10]  # Fetching first 10 categories for display
  
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'categories': categories,
        'page_obj': page_obj
    }
    return render(request, 'catalog/index.html', context)


def product_detail(request, slug: str):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })