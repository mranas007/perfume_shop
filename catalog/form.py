from django.forms import ModelForm
from django import forms
from .models import Review
from django.utils.translation import gettext_lazy as _


class CreateUserReview(ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-colors',
                'placeholder': 'Your name'
            }),
            'rating': forms.HiddenInput(),  # Hidden since we use custom star rating
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-colors resize-none',
                'placeholder': 'Share your experience with this product...',
                'rows': 4
            })
        }
        labels = {
            'user_name': 'Your Name',
            'rating': 'Rating',
            'comment': 'Your Review'
        }