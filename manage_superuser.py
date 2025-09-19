# manage_superuser.py
import os
from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not email or not password:
    print("DJANGO_SUPERUSER_EMAIL or PASSWORD not set, skipping superuser creation")
else:
    user, created = User.objects.get_or_create(
        email=email,
        defaults={"is_staff": True, "is_superuser": True},
    )
    if created:
        print(f"Superuser {email} created.")
        user.set_password(password)
        user.save()
    else:
        print(f"Superuser {email} already exists. Updating password...")
        user.set_password(password)
        user.save()
