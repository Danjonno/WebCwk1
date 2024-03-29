from django.contrib import admin
# Register your models here.

from .models import Authors, Stories

admin.site.register(Authors)
admin.site.register(Stories)