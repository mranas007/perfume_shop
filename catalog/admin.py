from django.contrib import admin
from . import models

admin.site.site_header = "Administration"
# admin.site.site_title = "Catalog Administration"
admin.site.index_title = "Adnan Perfume Administration"
admin.site.register(models.Category)
admin.site.register(models.Product)
