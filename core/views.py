from django.db.models import Q
from django.shortcuts import redirect, render
from catalog.models import Product, Category
from .form import ContactUsForm
from django.contrib import messages


def home(request):
  form = ContactUsForm()
  # Get up to 4 top listed products
  products = list(Product.objects.filter(top_listed=True)[:4])
  # If less than 4, fill with other products (excluding already selected)
  if len(products) < 4:
    needed = 4 - len(products)
    additional_products = Product.objects.exclude(id__in=[p.id for p in products])[:needed]
    products.extend(additional_products)
  context = {"products": products, "form": form}
  return render(request, 'core/home.html', context)


def about(request):
    context = {}
    return render(request, 'core/about.html', context)


def contact_us_submission(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "There was an error sending your message.")
    return redirect('home')