from django.shortcuts import render
from django.http import HttpResponse
# from django.db.models.aggregates import Count
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from store.filter import ProductFilter
from store.pagination import DefaultPagination
from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerizlizer, CreateOrderSerializer, OrderSerializer, ProductSerizlizer, ReviewSerializer, UpdateCartItemSerializer, CustomerUpdateSerializer, UpdateOrderSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView, DestroyAPIView, RetrieveAPIView, GenericAPIView,\
    ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from store import serializers

# Create your views here.
# **********************************************************************************************************************
# @api_view()   # this will replace following 'request' of Django with 'request' of DjangoRestFramework
# def product_list(request):
#     # return HttpResponse("ok")    # this is from Django
#     return Response("ok")

# @api_view()
# def product_details(request, id):
#     return Response(id)


# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# SERIALIZER ----> it converts model instance to Python Dictionary and then converting to JSON will happen under-the-hood by REST_FRAMEWORK


# ************************** PRODUCT **************************


# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related('collection').all()  # select_related is used becasue product can have only one collection and prefetch_related because a cart can have many CarItems
#         # serializer = ProductSerizlizer(queryset, many=True)  # many=True is because we want it to iterate over each product and convert all products into dicionary
#         serializer = ProductSerizlizer(queryset, many=True, context={'request':request})
#         # we are using context because it contains information about url 
#         # which we are using in ProductSerizlizer for collection field 
#         return serializer.data
#     elif request.method == "POST":
#         serializer = ProductSerizlizer(data=request.data)
#         # WAY 1
#         # if serializer.is_valid(raise_exception=True):
#         #     serializer.validated_data
#         #     return serializer.data
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # WAY 2
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         return serializer.data

# @api_view()
# def product_details(request, id):
#     # Method 1
#     # try:    # we are using try because if product with given id do not exist it will not break and instead this we can also use following Technique
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerizlizer(product)
#     #     return serializer.data
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#     # Method 2
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerizlizer(product)
#     return serializer.data


# ************************** COLLECTIONS **************************


# @api_view(['GET','POST'])  # here we are supporting only two http methods 
# def collection_list(request):
#     if request.method == "GET":
#         query_set = Collection.objects.annotate(products_count=Count("products")).all()
#         serializer = CollectionSerizlizer(query_set, many=True, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         # print(request.data)
#         serializer = CollectionSerizlizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")).all(), pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerizlizer(collection, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PUT":
#         serializer = CollectionSerizlizer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:  # remember orderitem is entity and _set defines relations automatically created by Django
#             return Response({"error":"Collection cannot be deleted because it is associciated with Some Products."}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************


# ************************** PRODUCT **************************


# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerizlizer(queryset, many=True, context={'request':request})   # we use context to provide additional data to serializer
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerizlizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()   # for saving coming product to DB
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         serializer = ProductSerizlizer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerizlizer(product, data=request.data)   # here we are updtaing our product 
#         serializer.is_valid(raise_exception=True)
#         serializer.save()   # for saving updated product to DB
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # ************************** COLLECTIONS **************************


# @api_view(['GET','POST'])  # here we are supporting only two http methods 
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(product_count=Count("products")).all()
#         serializer = CollectionSerizlizer(queryset, many=True, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         # print(request.data)
#         serializer = CollectionSerizlizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','PUT', 'DELETE'])
# def collection_detail(request, pk):   # .annotate(products_count=Count("products"))
#     collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerizlizer(collection, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PUT":
#         serializer = CollectionSerizlizer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:  # remember orderitem is entity and _set defines relations automatically created by Django
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# ALL the above was in Functional Approach so now we are going to use CLASS based approach


# ************************** PRODUCT **************************


# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerizlizer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ProductSerizlizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerizlizer(product)
#         return Response(serializer.data)
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerizlizer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitem_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ************************** COLLECTIONS **************************

# class CollectionList(APIView):
#     def get(self, request):
#         queryset = Collection.objects.annotate(product_count=Count("products")).all()
#         serializer = CollectionSerizlizer(queryset, many=True, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = CollectionSerizlizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#         serializer = CollectionSerizlizer(collection, context={"request":request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def put(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#         serializer = CollectionSerizlizer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#         if collection.products.count() > 0:  # remember orderitem is entity and _set defines relations automatically created by Django
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************


# as in above approach there  is a lot of repeatation and redundancy so now wee are going to use Model-Mixins and API-Views

# ************************** PRODUCT **************************

# class ProductList(ListCreateAPIView):
#     # WAY 1 if you don't  want to apply special functionalities
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerizlizer

#     # WAY 2  if you wants to apply some special functionalities
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
#     # def get_serializer_class(self):
#     #     return ProductSerizlizer
#     def get_serializer_context(self):
#         return {'request':self.request}

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerizlizer
#     # lookup_fields = 'id'  # you can use this is you particularly wants to use 'id' in urls.py instead of 'pk'

#     # we are using this function because it si particular to our delete method. It is not general like our get, create and update methods
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # ************************** COLLECTIONS **************************

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(product_count=Count("products")).all()
#     serializer_class = CollectionSerizlizer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count("products")).all()
#     serializer_class = CollectionSerizlizer
#     # lookup_fields = 'id'  # you can use this is you particularly wants to use 'id' in urls.py instead of 'pk'

#     # we are using this function because it si particular to our delete method. It is not general like our get, create and update methods
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#         if collection.products.count() > 0:
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# here we are using more better way because over above implemantion is also repeatating and redundent and can be merged

# ************************** PRODUCT **************************

# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerizlizer

#     def get_serializer_context(self):
#         return {'request':self.request}

#     # here we are using destroy and not delete because in ModelViewSet we have destroy
#     def destroy(self, request, *args, **kwargs):
#         # if product.orderitem_set.count() > 0:
#         if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:  # this implementation is because we have already quried that product
#             # from DB now we are not again querying but just getting that directly
#             return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)

#     # def delete(self, request, pk):
#     #     product = get_object_or_404(Product, pk=pk)
#     #     if product.orderitem_set.count() > 0:
#     #         return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     #     product.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)

# # ************************** COLLECTIONS **************************

# class CollectionViewSet(ModelViewSet):
#     queryset = Collection.objects.annotate(product_count=Count("products")).all()
#     serializer_class = CollectionSerizlizer

#     def destroy(self, request, *args, **kwargs):
#         # kwargs contain our URL parameters
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=kwargs['pk'])
#         if collection.products.count() > 0:
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)

#     # def delete(self, request, pk):
#     #     collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=pk)
#     #     if collection.products.count() > 0:
#     #         return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#     #     collection.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)


# # ************************** REVIEWS **************************
# class ReviewViewSet(ModelViewSet):
#     # queryset = Review.objects.all()   # we are not using this because we wants to show every product it own Reviews not 
#     # first product show all other products Reviews and second product show all other products Reviews and so on
#     # so we will filter this in below get_queryset method
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])

#     def get_serializer_context(self):
#         # kwargs contain our URL parameters
#         return {'product_id':self.kwargs['product_pk']}

# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************

# # ************************** PRODUCT **************************
# class ProductViewSet(ModelViewSet):
#     # queryset = Product.objects.select_related('collection').all()   # now we are not using this because we are setting query_params in url
#     serializer_class = ProductSerizlizer
#     queryset = Product.objects.all()   # we bring this back because now we are using DjangoFilterBackend
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     # filterset_fields = ['collection_id', 'unit_price'] # 'unit_price' will not work properly so we define custom filter 
#     filterset_class = ProductFilter
#     search_fields = ['title', 'description']  # can also add 'collection__title'
#     ordering_fields = ['unit_price', 'last_update']    # you can also apply multiple ordering filters like ---> ordering=-unit_price,last_update in URL.  - is for descending
#     pagination_class = DefaultPagination


#     # following is user definded (by me) filter but now as we are using DjangoFilterBackend so we dont need this
#     # def get_queryset(self):
#     #     queryset = Product.objects.select_related('collection').all()
#     #     # collection_id=self.request.query_params['collection_id']   # this will return error if 'collection_id' was not provided 
#     #     collection_id=self.request.query_params.get('collection_id')    # this will NOT return error if 'collection_id' was not provided 
#     #     if collection_id is not None:
#     #         queryset = queryset.filter(collection_id=collection_id)
#     #     return queryset

#     def get_serializer_context(self):
#         return {'request':self.request}

#     def destroy(self, request, *args, **kwargs):
#         if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0: 
#             return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)


# # ************************** COLLECTIONS **************************
# class CollectionViewSet(ModelViewSet):
#     queryset = Collection.objects.annotate(product_count=Count("products")).all()
#     serializer_class = CollectionSerizlizer

#     def destroy(self, request, *args, **kwargs):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=kwargs['pk'])
#         if collection.products.count() > 0:
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)


# # ************************** REVIEWS **************************
# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])

#     def get_serializer_context(self):
#         return {'product_id':self.kwargs['product_pk']}



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************




# # ************************** PRODUCT **************************
# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerizlizer
#     queryset = Product.objects.all() 
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = ProductFilter
#     search_fields = ['title', 'description']
#     ordering_fields = ['unit_price', 'last_update']
#     pagination_class = DefaultPagination
#     permission_classes = [IsAdminOrReadOnly]  # this is our user defined Permission class

#     def get_serializer_context(self):
#         return {'request':self.request}

#     def destroy(self, request, *args, **kwargs):
#         if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0: 
#             return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)


# # ************************** COLLECTIONS **************************
# class CollectionViewSet(ModelViewSet):
#     queryset = Collection.objects.annotate(product_count=Count("products")).all()
#     serializer_class = CollectionSerizlizer
#     permission_classes = [IsAdminOrReadOnly]  # this is our user defined Permission class

#     def destroy(self, request, *args, **kwargs):
#         collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=kwargs['pk'])
#         if collection.products.count() > 0:
#             return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)


# # ************************** REVIEWS **************************
# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])

#     def get_serializer_context(self):
#         return {'product_id':self.kwargs['product_pk']}


# # ************************** CART **************************
# class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):  # we are not using ModelViewSet becaues we dont want all operations but particular one
#     queryset = Cart.objects.prefetch_related('items__product').all() # here we are first prefetching items then further prefetching product for items
#     serializer_class = CartSerializer


# # ************************** CART-ITEM **************************
# class CartItemViewSet(ModelViewSet): 
#     # serializer_class = CartItemSerializer # we are not using this becasue now we have two serializers one for get and one for post
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return AddCartItemSerializer
#         elif self.request.method == "PATCH":
#             return UpdateCartItemSerializer
#         return CartItemSerializer

#     def get_serializer_context(self):
#         return {'cart_id':self.kwargs['cart_pk']}

#     def get_queryset(self):
#         return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')



# # ************************** CUSTOMER-UPDATE **************************
# # class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
# class CustomerViewSet(ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerUpdateSerializer
#     permission_classes = [IsAdminUser]  # this is for complete CustomerViewSet
#     # permission_classes = [FullDjangoModelPermissions]  # this is a bit advance topic

#     # def get_permissions(self):
#     #     if self.request.method == "GET":
#     #         return [AllowAny()]
#     #     return [IsAuthenticated()]

#     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])  # you can also set permissions to particular actions , permission_classes=[] 
#     # false means it will be available in list-view like ----> http://127.0.0.1:8000/store/customers/me/
#     # and if it is True it will be available in detail-view ----> http://127.0.0.1:8000/store/customers/1/me/
#     def me(self,request):
#         (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
#         if request.method == 'GET':
#             serializer = CustomerUpdateSerializer(customer)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = CustomerUpdateSerializer(customer, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)





# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************








# ************************** PRODUCT **************************
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerizlizer
    queryset = Product.objects.all() 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0: 
            return Response({"error":" Product cannot be deleted because it is associciated with Some Order."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# ************************** COLLECTIONS **************************
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count("products")).all()
    serializer_class = CollectionSerizlizer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(product_count=Count("products")).all(), pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({"error":" Collection cannot be deleted because it is associciated with Some Products. "}, status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# ************************** REVIEWS **************************
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


# ************************** CART **************************
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


# ************************** CART-ITEM **************************
class CartItemViewSet(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')



# ************************** CUSTOMER-UPDATE **************************
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self,request):
        # (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerUpdateSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerUpdateSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



# ************************** ORDER **************************
class OrderViewSet(ModelViewSet):
    head_method_names = ['get', 'put', 'post', 'patch', 'delete', 'head', 'options']
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id':self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()   # we are returing this order from save() method in ---> CreateOrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PUT":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        # (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************



# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************