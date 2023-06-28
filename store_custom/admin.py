from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProcductAdmin
from tags.models import TaggedItem
from store.models import Product

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    
class CustomProductAdmin(ProcductAdmin):
    inlines = [TagInline]
    
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
