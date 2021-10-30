from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet, prefetch_related_objects
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TaggedItem
from . import models


# search Django ModelAdmin ---------> GOOGLE

# Register your models here.


# *********************************************************************************************************************
admin.site.register(models.Cart)

# *********************************************************************************************************************
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            # ('actualValueForFiltering', 'humanReadAbleNameforFiltering')
            ('<10', 'Low')  # this field will appear in filtering
        ]

    def queryset(self, request, queryset:QuerySet):
        if self.value() == '<10':  # here is the actual implementation for above filtering, there can be many others too
            return queryset.filter(inventory__lt=10)

# class TagsInline(GenericTabularInline):
#     model = TaggedItem
#     autocomplete_fields = ['tag']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines  = [TagsInline]   # as we are using it here directly its making our app dependent on eachOther so we created core app and it there
    # fields = ['slug', 'title']     # only these fields will be shown for creating new Product
    # exclude = ['promotions']    # all fields will be shown for creating new Product EXCEPT these or this
    # readonly_fields = ['slug']    # this option is for read only
    prepopulated_fields = {   # for pre-populating fields
        'slug':['title'],   # here you can give more fields like unit_price and others too
    }
    autocomplete_fields = ['collection']  # as you are using 'collection' here you will have to define search_fields in the CollectionAdmin below
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']  
    # 'inventory' is replaced with 'inventory_status'
    # 'collection' is replaced with 'collection_title'
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['product']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


# *********************************************************************************************************************
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'member_ship', 'orders']   
    # here we didn't use this approach 'user__first_name' because currently it is not supported 
    # so we defined methods in Customer Model
    list_editable = ['member_ship']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
    autocomplete_fields = ['user']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = ( reverse('admin:store_order_changelist') + '?' + urlencode({ 'customer__id': str(customer.id) }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

# *********************************************************************************************************************
class OrderInline(admin.TabularInline):   # there is also 'StackedInline'
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0     # this is for removing pre available inputs
    min_num = 1   # this is for minimum orders to add
    max_num = 10  # this is for maximun orders to add
    # readonly_fields = ['unit_price']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderInline]   # this is used for adding OrderItem to Order at admin panel below # Just check it
    autocomplete_fields = ['customer']



# *********************************************************************************************************************
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # return collection.prod_count
        # reverse('admin:appName_modelName_pageName')   # this will return url of that particular product in admin page
        url = reverse('admin:store_product_changelist') + '?' + urlencode({ 'collection__id': str(collection.id) })
        return format_html('<a href={}>{}</a>', url, collection.prod_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            prod_count=Count('product')
        )
