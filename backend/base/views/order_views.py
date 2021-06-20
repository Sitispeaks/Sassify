from datetime import datetime
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer,OrderSerializer

from rest_framework import serializers, status
import datetime



"""This is Order view"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user=request.user
    data=request.data


    orderItems=data['orderItems']
    if orderItems and len(orderItems)==0:
        return Response({'detail':'No Order Items'},status=status.HTTP_400_BAD_REQUEST)
    else :


        # from the given data
        #(1)create order

        order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

        #(2)create shipping address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            pinCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        #(3)create order items and and create the order& orderitem relationship
        for i in orderItems:
            product = Product.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

        #(4) update stock of that product
            
            product.countInStock -= item.qty
            product.save()
        serializer=OrderSerializer(order,many=False)
        # print(serializer.data)

        return Response(serializer.data)




"""api/orders/myorders/"""
"""get al orders in profile section"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user=request.user
    """as order is in many to one relationship with user"""
    """so we can retrive all order by this"""
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/
    orders=user.order_set.all()
    # print(orders)
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)


"""For Admin view"""
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders=Order.objects.all()
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)




"""get order by id"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,pk):
    user=request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user==user:
            serializer=OrderSerializer(order,many=False)
            return Response(serializer.data)
        else:
            Response({'detail':'Not authorized to see the order!'},status=status.HTTP_400_BAD_REQUEST)
    except :
        return Response({'detail':'Order does not exists'},status=status.HTTP_400_BAD_REQUEST)




"""/api/orders/:id/pay/"""
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,pk):
    order = Order.objects.get(_id=pk)
    # print(order)
    order.isPaid=True
    order.paidAt=datetime.datetime.now()
    order.save()
    return Response('Order was paid')





@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderStatus(request,pk,status):
    order = Order.objects.get(_id=pk)
    order.order_status=status
    if status=="delivered":
        order.isDelivered=True
        order.deliveredAt=datetime.datetime.now()
    order.save()
    return Response('Order status updated')

