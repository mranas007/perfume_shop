from django.shortcuts import render
from .models import Customer_feedback



def index(request):
    feedback_list = Customer_feedback.objects.filter(add_to_list=True)
    return render(request, 'feedback/index.html', {'feedback_list': feedback_list})


def customer_feedback(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        user = request.user

        # Save feedback to the database
        feedback = Customer_feedback(
            product_id=product_id,
            user=user,
            rating=rating,
            comment=comment
        )
        feedback.save()

    # Fetch all feedback for the product
    feedback_list = Customer_feedback.objects.filter(product_id=product_id)

    return render(request, 'feedback/customer_feedback_form.html', {'feedback_list': feedback_list})