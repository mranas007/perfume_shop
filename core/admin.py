from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_per_page = 20
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)

admin.site.register(ContactUs, ContactUsAdmin)
