from django.shortcuts import render, redirect
from perfume_shop import settings
from .models import User
from .form import CustomUserCreationForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from accounts.utils import send_mail_to_client
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str





def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists with the provided email
        if check_user := User.objects.filter(email=email).first():
            if check_user.is_active:
                user = authenticate(email=email, password=password)
            else:
                messages.error(request, 'Account is inactive, Please Activate your account.')
                return redirect('accounts:login')
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            messages.success(request, "Registration successful.")
            return redirect('email_confirmation_alert')
        else:
            messages.error(request, 'Something went wrong please try again later.')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


# This function is used to send an account activation email
def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Used reverse() instead of hardcoding
    activation_path = reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
    activation_link = f"{settings.SITE_DOMAIN}{activation_path}"

    send_mail_to_client(
        subject="Activate your account",
        message=f"Click the link to activate your account: {activation_link}",
        recipient_list=[user.email],
    )


# This function is used to activate a user account
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:login')


# This function is used to render an email confirmation alert page
def email_confirmation_alert(request):
  return render(request, 'accounts/email_confirmation_alert.html')


# This function is used to resend the activation email
def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if check_user := User.objects.filter(email=email).first():
            if check_user.is_active:
                messages.success(request, "Your email is already activated.")
                return redirect('accounts:login')
            
            send_activation_email(request, check_user)
            messages.success(request, "Activation email resent.")
            return redirect('accounts:login')
        else:
            messages.error(request, "No user found with this email address.")
    return render(request, 'accounts/resend_activation_email.html')


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
