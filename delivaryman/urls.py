
from django.urls import path
from .views import *
from order import views
from order.views import *
# from .views import  CreateCheckOutSession 


urlpatterns = [
    path('failed/<int:order_id>', orderFailed),
    path('delivered/<int:order_id>', orderDelivered),
    path('list/', listShippedOrders),
]