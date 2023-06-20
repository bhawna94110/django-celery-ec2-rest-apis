from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Customer
from django.db.models import Q, F, Value, Func #stands for query 
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem

# Create your views here.
#request -> response
#request handler
#action

def say_hello(request):
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.filter(unit_price__range=(20, 30))
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(last_update__year=2021)
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # query_set = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))
    #You want to compare two feildes of a single model?
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    
    #sorting
    # query_set = Product.objects.order_by('title')
    #sort by desc
    # query_set = Product.objects.order_by('-title')
    
    #add new col
    # query_set = Product.objects.annotate(new_id=F('id') + 1)
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'),Value(' '),
    #                F('last_name'), function='CONCAT')
    # )
    
    #quering generic relationship
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)
    
    # queryset cache
    queryset = Product.objects.all()
    queryset[0]
    list(queryset)
    return render(request,'hello.html', {'name':'Bhawna'})