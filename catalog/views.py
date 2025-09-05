from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q



def catalog_page(request):
    category_slug = request.GET.get('category_slug', '')
    sort_by = request.GET.get('sort', 'featured')
    search_query = request.GET.get('q')

    # Base queryset
    products = Product.objects.all()

    # Apply category filter
    if category_slug:
        products = products.filter(category__slug=category_slug)
        current_category = Category.objects.filter(slug=category_slug).first()
    else:
        current_category = None

    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popular':
        products = products.order_by('-top_listed', '-created_at')  # Assuming top_listed indicates popularity
    else:  # featured/default
        products = products.order_by('-top_listed', '-created_at')

    categories = Category.objects.all()[:10]  # Fetching first 10 categories for display

    # Pagination
    paginator = Paginator(products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,  # Full queryset for sidebar counts
        'categories': categories,
        'page_obj': page_obj,
        'current_category': current_category,
        'sort_by': sort_by
    }
    return render(request, 'catalog/index.html', context)


def product_detail(request, slug: str):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })