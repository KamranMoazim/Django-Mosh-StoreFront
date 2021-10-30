from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from store.models import Product
from tags.models import TaggedItem
from store.admin import ProductAdmin
from . import models

# Register your models here.

# admin.site.register(models.User)
@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    # pass 
    # we got following code from BaseUserAdmin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )


class TagsInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

class CustomProductAdmin(ProductAdmin):
    inlines = [TagsInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
