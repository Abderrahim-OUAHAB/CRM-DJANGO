from django.contrib import admin

from .models import Produit,Tag
# Register your models here.
admin.site.register(Produit)
admin.site.register(Tag)