from django.shortcuts import render, redirect
from perfume_shop import settings
from .models import User
from .form import CustomUserCreationForm, EditUserForm, SetPassword, LoginForm
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



def login_view(request): # Login View
    if request.user.is_authenticated:
        return redirect('home')  
    
    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Check if the user exists with the provided email
            if check_user := User.objects.filter(email=email).first():
                if check_user.is_active:
                    user = authenticate(email=email, password=password)
                    if user is None:
                        form.add_error("password", "Invalid password.")
                        messages.error(request, 'Invalid password.')
                        return redirect('accounts:login')
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, 'Account is inactive, Please Activate your account.')
                    return redirect('accounts:login')
            else:
                form.add_error("email", "Invalid email.")
                messages.error(request, 'Invalid email.')
                return redirect('accounts:login')

    return render(request, 'accounts/login.html', {"form": form})



def register_view(request): # Registration View
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if user is already logged in

    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User needs to activate via email
            user.save()
            send_activation_email(request, user)
            messages.success(request, "Registration successful. Please check your email to activate your account.")
            return redirect('accounts:email_confirmation')
        else:
            messages.error(request, 'Something went wrong please try again later.')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)



def email_confirmation_alert(request): # To render an email confirmation alert page
  return render(request, 'accounts/email_confirmation_alert.html')



def send_activation_email(request, user): # To send an account activation email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Used reverse() instead of hardcoding
    activation_path = reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
    activation_link = f"{settings.SITE_DOMAIN}{activation_path}"

    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #d97706;">Welcome to Adnan Perfume!</h2>

            <p>Dear <strong>{user.name}</strong>,</p>

            <p>Thank you for registering with Adnan Perfume! We're excited to have you join our community of fragrance enthusiasts.</p>

            <p>To complete your registration and activate your account, please click the button below:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{activation_link}" style="background-color: #d97706; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Activate Your Account</a>
            </div>

            <p style="color: #666; font-size: 14px;">This link will expire in 7 days for security reasons.</p>

            <p>If you did not create an account with us, please ignore this email.</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

            <p>For any questions or support, please contact us at <a href="mailto:adnanperfume84@gmail.com" style="color: #d97706;">adnanperfume84@gmail.com</a>.</p>

            <p>Best regards,<br>
            <strong>Adnan Perfume Team</strong><br>
            <a href="https://perfumeshop-production-a97b.up.railway.app/" style="color: #d97706;">https://perfumeshop-production-a97b.up.railway.app/</a></p>
        </div>
    </body>
    </html>
    """

    try:
        send_mail_to_client(
            subject="Activate your account",
            message="Please check your email and click the activation link to activate your account.",  # Plain text fallback
            recipient_list=[user.email],
            html_message=html_message,
        )
    except Exception as e:
        raise  # Re-raise to let Django handle it



def activate_account(request, uidb64, token): # To activate a user account
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



def resend_activation_email(request): # To resend the activation email
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



def forgot_password_view(request): # To render the forgot password page
    if request.method == 'POST':
        email = request.POST.get('email')
        if user := User.objects.filter(email=email).first():
            # Send password reset email
            send_password_reset_email(request, user)
            messages.success(request, "Password reset email sent.")
            return redirect('accounts:login')
        else:
            messages.error(request, "No user found with this email address.")
    return render(request, 'accounts/forgot_password.html')



def send_password_reset_email(request, user): # To send a password reset email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Used reverse() instead of hardcoding
    reset_path = reverse("accounts:reset_password", kwargs={"uidb64": uid, "token": token})
    reset_link = f"{settings.SITE_DOMAIN}{reset_path}"
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #d97706;">Password Reset Request</h2>

            <p>Dear <strong>{user.name}</strong>,</p>

            <p>We received a request to reset your password for your Adnan Perfume account. If you made this request, please click the button below to reset your password:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #d97706; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Reset Your Password</a>
            </div>

            <p style="color: #666; font-size: 14px;">This link will expire in 7 days for security reasons.</p>

            <p>If you did not request a password reset, please ignore this email. Your password will remain unchanged.</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

            <p>For any questions or support, please contact us at <a href="mailto:adnanperfume84@gmail.com" style="color: #d97706;">adnanperfume84@gmail.com</a>.</p>

            <p>Best regards,<br>
            <strong>Adnan Perfume Team</strong><br>
            <a href="https://perfumeshop-production-a97b.up.railway.app/" style="color: #d97706;">https://perfumeshop-production-a97b.up.railway.app/</a></p>
        </div>
    </body>
    </html>
    """
    try:
        send_mail_to_client(
            subject="Reset your password",
            message="Please check your email and click the password reset link to reset your password.",  # Plain text fallback
            recipient_list=[user.email],
            html_message=html_message,
        )
    except Exception as e:
        raise



def reset_password_view(request, uidb64, token): # To reset a user's password
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPassword(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('accounts:login')
        else:
            form = SetPassword()

        return render(request, 'accounts/reset_password.html', {'form': form})
    else:
        messages.error(request, 'Password reset link is invalid!')
        return redirect('accounts:login')



def logout_view(request): # To log out a user
    logout(request)
    return redirect('accounts:login')


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