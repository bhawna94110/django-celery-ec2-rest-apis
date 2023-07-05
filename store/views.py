from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from . models import Product, Collection, Review, Cart, CartItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer
from django.db.models.aggregates import Count
from .models import OrderItem
from .filters import ProductFilter
from .pagination import DefaultPagination
from.permissions import IsAdminOrReadOnly, ViewCustomHistoryPermissions

## PUT ALL THE SAME OR RELATED LOGIC IN ONE CLASS with the help of VIEWSETS
class ProductViewSet(ModelViewSet):
    #Adding generic filters, we dont need to add get_queryset function for query params
    #But if need unit price filtering in between some range, we need to do custom filtering for that.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination #if you want to add pagination only for particular class
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    
    # function for adding query params
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    # def destroy(self, request, *args, **kwargs):
    #     if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
    #         return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().destroy(request, *args, **kwargs)
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection can not be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    @action(detail=True, permission_classes=[ViewCustomHistoryPermissions])
    def history(self, request, pk):
        return Response('ok')
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        if request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

####GENERIC API VIEWS
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer(self, *args, **kwargs):
#     #     return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id' we can do this for particular field, like we are giving pk as id but django expect it as pk.
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
    
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

##### CLASS API VIEWS    
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetails(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#### FUNCTION BASED VIEWS
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
      
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    