from django.db.models import Q
from django.shortcuts import redirect, render
from catalog.models import Product, Category
from .form import ContactUsForm
from django.contrib import messages


def home(request):
  product_to_list = 4
  form = ContactUsForm()
  # Get up to 4 top listed products
  products = list(Product.objects.filter(top_listed=True)[:product_to_list])
  # If less than 4, fill with other products (excluding already selected)
  if len(products) < product_to_list:
    needed = product_to_list - len(products)
    additional_products = Product.objects.exclude(id__in=[p.id for p in products])[:needed]
    products.extend(additional_products)
  context = {"products": products, "form": form}
  return render(request, 'core/home.html', context)


def about(request):
    context = {}
    return render(request, 'core/about.html', context)


def contact_us_submission(request):

      form = ContactUsForm(request.POST or None)
      return_url = request.POST.get('returnUrl') or request.META.get('HTTP_REFERER')

      if request.method == "POST":
        if form.is_valid():
          form.save()
          messages.success(request, "Your message has been sent successfully!")
        else:
          messages.error(request, "Please fill out all fields correctly.")

        if return_url:
          return redirect(return_url)

      return render(request, 'core/contact_us.html', {'form': form})






