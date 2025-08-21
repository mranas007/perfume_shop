from django.shortcuts import render, redirect
from .models import User
from accounts.models import User
from .form import CustomUserCreationForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists with the provided email
        if User.objects.filter(email=email).exists():
            user = authenticate(email=email, password=password)
        else:
            messages.error(request, 'Email does not exist.')
            return redirect('accounts:login')

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            # Invalid login
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')  # Redirect if user is already logged in
    
    form = CustomUserCreationForm()
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong please try again later.')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='accounts:login')
def profile_view(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def update_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditUserForm(instance=user)

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='accounts:login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
