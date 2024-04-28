from django.contrib import admin

from .models import Order,OrderItem,OrderItemTmp,OrderTmp

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderTmp)
admin.site.register(OrderItemTmp)

