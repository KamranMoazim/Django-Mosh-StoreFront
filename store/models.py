from uuid import uuid4
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator  # seasrch Django Validators
# Create your models here.


# search ---------> Django Field Types   ---------> to get all fields types

# ****************************************************************************************************************
# MANY-TO-MANY ------> a product can have many products and reverse a promotion can be set to many products
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # here we will have reverse-relation field like -----> product_set   which you can change through related_name="products"


# ****************************************************************************************************************
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True) # null=True is for DB but for Django Admin we need blank=True
    # 9999.99 
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)    
    # **auto_now** is for only every time 
    # **auto_now_add** is for only first time
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# ****************************************************************************************************************
# ONE-TO-MANY ------> a collection can have many products
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # here we will have reverse-relation field like -----> product_set   which you can change through related_name="products"
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# ****************************************************************************************************************
# ONE-TO-MANY ------> a cart can have many order-items
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


# ****************************************************************************************************************
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # cartitem_set
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]  # it will make sure that you have one unique product in each cart


# ****************************************************************************************************************
# ONE-TO-MANY ------> a customer can have many orders
# class Customer(models.Model):
#     MEMBERSHIP_BRONZE = 'B'
#     MEMBERSHIP_SILVER = 'S'
#     MEMBERSHIP_GOLD = 'G'
#     MEMBERSHIP_CHIOCES = {
#         (MEMBERSHIP_BRONZE, 'Bronze'),
#         (MEMBERSHIP_SILVER, 'Silver'),
#         (MEMBERSHIP_GOLD, 'Gold'),
#     }
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)
#     birth_date = models.DateTimeField(null=True)
#     member_ship = models.CharField(max_length=1, choices=MEMBERSHIP_CHIOCES, default=MEMBERSHIP_BRONZE)
#     # here we dont need address field because DJANGO automatically creates inverse relation 
#     # ----> as we have already created customer field in Address 

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

#     class Meta:
#         ordering = ['first_name', 'last_name']

# making changings because we have added our Custom User Model
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHIOCES = {
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    }
    # we removed some fields because they are already defined in our User Model
    phone = models.CharField(max_length=15)
    birth_date = models.DateTimeField(null=True)
    member_ship = models.CharField(max_length=1, choices=MEMBERSHIP_CHIOCES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


# ****************************************************************************************************************
# ONE-TO-MANY ------> a order can have many order-items
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAIL = 'F'
    PAYMENT_STATUS = {
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAIL, 'Fail'),
    }
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            # (code_name, description)
            ('cancel_order', 'can cancel order')
        ]


# ****************************************************************************************************************
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)  # , related_name='orderitems'
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()


# ****************************************************************************************************************
######## ****** here one customer can have only one address ******
# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) 
#     # ---------> what should happen when we delete a Customer
#     # one address can belong to only one Customer so ----> OneToOneField
#     # primary_key=True ---> is compulsory because if we DID NOT use this than we will have many addresses for one customer
######## ****** here one customer can have many addresses ******
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    # ---------> what should happen when we delete a Customer
    


# ****************************************************************************************************************
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)