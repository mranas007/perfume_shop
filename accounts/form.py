import re
from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure Name is the initially focused field
        for f in self.fields.values():
            try:
                self.fields[f.name].widget.attrs.pop('autofocus', None)
            except Exception:
                pass
        if 'name' in self.fields:
            self.fields['name'].widget.attrs['autofocus'] = True
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '') or ''
        # Keep digits only
        normalized = re.sub(r'\D', '', phone)
        if not (11 <= len(normalized) <= 15):
            raise forms.ValidationError('Enter a valid phone number (11-15 digits).')
        # Optional: ensure unique phone
        if User.objects.filter(phone=normalized).exists():
            raise forms.ValidationError('This phone number is already in use.')
        # Replace with normalized value
        return normalized


class SetPassword(ModelForm):
        class Meta:
            model = User
            fields = ['password']
            widgets = {
                'password': forms.PasswordInput(attrs={'placeholder': 'New password'}),
            }


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone']


class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
