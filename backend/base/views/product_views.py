from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Product, Review
from base.serializers import ProductSerializer,ProductDocumentSerializer

from rest_framework import status
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from base.documents import ProductDocument

from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SuggesterFilterBackend,
    CompoundSearchFilterBackend
)


"""This is product view accessible by everyone"""
# product view
serializer_class=ProductSerializer
@api_view(['GET'])
def getProducts(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    product=Product.objects.get(id=pk)
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getTopProducts(request):
    """rating_gte == rating greater than equals to"""
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user=request.user
    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request,pk):
    data=request.data
    product=Product.objects.get(id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()
    
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request,pk):
    product=Product.objects.get(id=pk)
    product.delete()
    return Response('Product deleted successfully!')

serializer_class=ProductSerializer
@api_view(['POST'])
def uploadImage(request):
    data=request.data

    product_id=data['product_id']
    product=Product.objects.get(id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    
    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    data=request.data

    #1- Review already exists
    alreadyExists= product.review_set.filter(user=user).exists()
    if alreadyExists:
        content={'detail':'You have already reviewed the product'}
        return Response(content,status.HTTP_400_BAD_REQUEST)

    #2- No rating or 0

    elif data['rating']==0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #3 Create review
    else:
        review=Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total=0
        for i in reviews:
            total+=i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')

    



class ProductDocumentView(DocumentViewSet):
    document=ProductDocument
    serializer_class=ProductDocumentSerializer

    filter_backends=[
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        'name',
        'brand',
        'description',
    )
    multi_match_search_fields = (
       'name',
       'brand',
       'description',
    )

    filter_fields ={
        'name':'name',
        'brand':'brand',
        'description':'description',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)