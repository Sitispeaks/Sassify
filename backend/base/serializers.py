from django.db import models
from django.db.models import fields
from elasticsearch_dsl import document
from  rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,User,OrderItem,ShippingAddress,Order,Review
from rest_framework_simplejwt.tokens import RefreshToken
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *


class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin']
        # these above fields are coming from token,then it goes to views,then to User model


    # here obj is the user model and self is the UserSerializer
    def get_name(self,obj):
        name=obj.first_name
        if name== '':
            name=obj.email

        return name

    def get__id(self,obj):
        _id=obj.id
        return _id
    
    def get_isAdmin(self,obj):
        return obj.is_staff


# This is for refresh tokens: when we change username or forgot password
class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields=['id','_id','username','email','name','isAdmin','token']

    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=Product
        fields='__all__'

    def get_reviews(self,obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields='__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'


class ChoicesField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        """init."""
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        """Used while retrieving value for the field."""
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in self._choices:
            if i == data or self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))



"""nested serializer"""
class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    order_status=ChoicesField(choices=Order.ORDER_STATUS)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address =ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data



"""Elasticsearch document serializer"""

class ProductDocumentSerializer(DocumentSerializer):
    class Meta:
        model=Product
        document=ProductDocument

        fields = [
                'id',
                'name',
                'image',
                'brand',
                'category',
                'description',
                'rating',
                'numReviews',
                'countInStock',
                'price'
        ]