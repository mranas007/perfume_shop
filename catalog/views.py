from django.shortcuts import render
from catalog.form import CreateUserReview
from .models import Product, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache


from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q
from .models import Product, Category

def catalog_page(request):
    category_slug = request.GET.get('category_slug', '')
    sort_by = request.GET.get('sort', 'featured')
    search_query = request.GET.get('q')
    page_number = request.GET.get('page', 1)

    # Cache key includes category, sort, search, and page
    cache_key = f"catalog_{category_slug}_{sort_by}_{search_query}_page_{page_number}"
    page_obj = cache.get(cache_key)

    if page_obj is None:
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
        match sort_by:
            case 'price_low':
                products = products.order_by('price')
            case 'price_high':
                products = products.order_by('-price')
            case 'newest':
                products = products.order_by('-created_at')
            case 'popular':
                products = products.order_by('-top_listed', '-created_at')
            case _:  # featured/default
                products = products.order_by('-top_listed', '-created_at')

        # Pagination
        paginator = Paginator(products, 20)  # 20 products per page
        page_obj = paginator.get_page(page_number)
        # Cache only this page result
        cache.set(cache_key, page_obj, 300)  # 5 minutes

    # Cache categories list separately
    categories = cache.get('categories_list')
    if categories is None:
        categories = Category.objects.all()[:10]  # Sidebar categories
        cache.set('categories_list', categories, 3600)  # Cache for 1 hour

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'sort_by': sort_by,
    }
    return render(request, 'catalog/index.html', context)


def product_detail(request, slug: str):
    product = get_object_or_404(Product, slug=slug)
    customer_feedback = product.reviews.filter(active=True).order_by('-created_at')[:5]
    review_form = CreateUserReview()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    
    if request.method == 'POST':
        review_form = CreateUserReview(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            review_form = CreateUserReview()
            
            # Optionally, redirect to avoid re-submission on refresh
            # return redirect('catalog:product_detail', slug=slug)
    
    context = {
        'product': product,
        'customer_feedback': customer_feedback,
        'related_products': related_products,
        'review_form': review_form,
    }
    return render(request, 'catalog/product_detail.html', context)