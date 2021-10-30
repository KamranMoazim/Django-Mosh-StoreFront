from decimal import Decimal
from rest_framework import fields, serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from store import models
from django.db import transaction
from store.signals import order_created


# SERIALIZERS are actually API-Modles not That Models which we define in models.py file
# SERIALIZERS modles are for sending and receiving API data
# modles.py modles are for Actual DB storage models

# *******************************************************************************************************************
# class CollectionSerizlizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

# class ProductSerizlizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     # unit_price = serializers.DecimalField(max_digits=6 ,decimal_places=2)
#     price = serializers.DecimalField(max_digits=6 ,decimal_places=2, source='unit_price')  # we used this if we wants to change the field name for our API model
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  # this field is not defined in Actual DB field but this is specific for our API
#     # WAY 1 -----> which will show only the id like 1, 2, 3
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # )
#     # WAY 2 -----> which will show only the name like men, children, women
#     # collection = serializers.StringRelatedField()  # now when you use this without select_related or prefetch_relted 
#     # in views.py where actual queryset is executing then you will have 1000000000 many queries, so use 
#     # select_related or prefetch_relted in views.py queryset with serializer
#     # WAY 3 -----> which will show complete object
#     # collection = CollectionSerizlizer()
#     # WAY 4 -----> which will show link and by clicking on link you will move to that collection
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name='collection-detail'   # this is used for generating hyperlinks
#     )

#     def calculate_tax(self, product:Product):
#         return product.unit_price * Decimal(1.1)  # we converted 1.1 to Deciamal because by-default it was float and product.unit_price is Decimal so both must be same for multiplication


# *******************************************************************************************************************
# now are using ModelSerializer instead of  simple Serializer because it gives us following facilty which you can see 
# class CollectionSerizlizer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ['id', 'title', 'product_count']

#     product_count = serializers.IntegerField(read_only=True)


# class ProductSerizlizer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection', 'inventory', 'description', 'slug']  # , 'price'
#     # here we are giving only those fields from our DB-Model which we want in our API-Model and if it does not find that field in 
#     # our DB-Model so it will use following definition like in case of price_with_tax and price because we have only unit_price 
#     # in our DB-Model
#     # price = serializers.DecimalField(max_digits=6 ,decimal_places=2, source='unit_price', read_only=True)
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax', read_only=True)  
#     # collection = serializers.HyperlinkedRelatedField(
#     #     queryset = Collection.objects.all(),
#     #     view_name='collection-detail'
#     # )

#     def calculate_tax(self, product:Product):
#         return product.unit_price * Decimal(1.1)


# *******************************************************************************************************************
# ********************************************* COLLECTION
class CollectionSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
    product_count = serializers.IntegerField(read_only=True)

# ********************************************* PRODUCT
class ProductSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection', 'inventory', 'description', 'slug']  # , 'price'
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax', read_only=True)  

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)

# ********************************************* REVIEW
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'date', 'description']  # , 'product'

    def create(self, validated_data):
        product_id = self.context['product_id']   # we are getting this from views.py ---> ReviewViewSet
        return Review.objects.create(product_id=product_id, **validated_data)


# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

# ********************************************* CART-ITEM
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()  # (method_name='get_total_price')

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price



# ********************************************* CART
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    # def get_Name_of_Field   # for defining method for field
    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


# ********************************************* Add-Item-to-CART
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # def validate_Name_of_Field  # for defining method for validating particular field
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No Product with given Id Exists.")
        return value

    # we are over-riding this method because we wants to update item quantity not just add same item again to cart
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # update cart-quantity
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item  # we are using self.instance becasue this is how it is implemented in ModelSerializer
        except CartItem.DoesNotExist:
            # create new cart-item
            # CartItem.objects.get(cart_id=cart_id, product_id=product_id, quantity=quantity)  # way 1
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)  # way 2
            self.instance = cart_item

        return self.instance


    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']



# ********************************************* Updating-Item-to-CART
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']



# ********************************************* Updating-CUSTOMER
class CustomerUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'birth_date', 'member_ship', 'phone']
    



# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************
# *******************************************************************************************************************

# ********************************************* ORDERS-ITEM

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

# ********************************************* ORDERS
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']


# ********************************************* UPDATE-ORDER
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']




# ********************************************* CREATE-ORDERS
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            # (customer, created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [OrderItem(order=order, product=item.product, unit_price=item.product.unit_price, quantity=item.quantity) for item in cart_items]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
