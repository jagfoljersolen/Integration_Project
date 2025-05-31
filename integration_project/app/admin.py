from django.contrib import admin

# Register your models here.

from .models import Conflict, Commodity

admin.site.register(Conflict)
admin.site.register(Commodity)