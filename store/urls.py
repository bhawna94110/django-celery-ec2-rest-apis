from django.urls import path
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]
