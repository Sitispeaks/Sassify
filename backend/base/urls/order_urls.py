from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('orders/',views.getOrders,name="orders"),
    path('orders/add/',views.addOrderItems,name='orders-add'),
    path('orders/myorders/',views.getMyOrders,name="my-orders"),
    
    path('orders/<str:pk>/',views.getOrderById,name='user-order'),
    # path('orders/<str:pk>/deliver/',views.updateOrderToDelivered,name='order-deliver'),
    path('orders/<str:pk>/pay/',views.updateOrderToPaid,name='order-pay'),
    path('orders/<str:pk>/<str:status>/',views.updateOrderStatus,name="order-status"),
]