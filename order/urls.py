
from django.urls import path
from . import views
from .views import  CreateCheckOutSession 


urlpatterns = [
    path('orders/new/',views.new_order, name='new_order'),
    path('orders/newTmp/',views.new_orderTmp, name='new_orderTmp'),
    path('orders/',views.get_orders, name='get_orders'),
    path('userorders/',views.get_user_orders, name='get_user_orders'),
    path('orders/Tmp',views.get_ordersTmp, name='get_ordersTmp'),
    path('orders/<str:pk>/',views.get_order, name='get_order'),
    path('orders/orderTmp/',views.get_orderTmp, name='get_orderTmp'),
    path('orders/<str:pk>/process/',views.process_order, name='process_order'),
    path('orders/<int:product_id>', views.shipProduct),
    path('shiporders/<int:order_id>', views.shipOrder),
    path('refundmoney/<int:order_id>', views.refundMoney),
    path('orders/items',views.vendor_orderItems, name='vendor_orderItems'),
    path('orders/<str:pk>/delete/',views.delete_order, name='delete_order'),
    path('orders/<str:pk>/deleteTmp/',views.delete_orderTmp, name='delete_orderTmp'),
    path('create-checkout-session/<pk>/',CreateCheckOutSession.as_view(), name='checkout_session'),
    path('orders/<str:pk>/cancel/',views.cancelOrder, name='cancel_order'),  # Add cancel order URL
]