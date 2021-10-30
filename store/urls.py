from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

# following uses FUNTIONAL based views
# urlpatterns = [
#     path('products/', views.product_list),
#     path('products/<int:pk>/', views.product_details),
#     path('collections/', views.collection_list),
#     path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]


# following uses CLASS based views
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]


# following uses MIXINS and GenericAPI based views
# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('carts', views.CartViewSet, basename='carts')

# routers.NestedDefaultRouter(parentRouter, parentPrefix, lookups='product')    
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')   # lookup means we will have id like product_id
products_router.register('reviews', views.ReviewViewSet, basename='products-reviews')  
# from basename we will have two mores like products-reviews-list and products-reviews-details like we started working from TOP, 
# and it will be by default

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')   # lookup means we will have id like product_id
carts_router.register('items', views.CartItemViewSet, basename='cart-items')  


# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
]
