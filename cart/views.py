from django.shortcuts import render

# Create your views here.
def cart_details(request):
    return render(request, 'cart/cart_detail.html')
