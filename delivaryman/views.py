from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from order.models import *
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsDeliveryMan
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from order.serializers import *
from django.core.mail import send_mail
from rest_framework import status
from django.db.models import Q



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listShippedOrders(request):
    orders = Order.objects.filter(Q(status='D') | Q(status='S') | Q(status='F')).order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['PUT'])
@permission_classes([IsDeliveryMan])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def orderFailed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.SHIPPED_STATE:
        order.status = Order.FAILED_STATE
        order.save()
        for item in order.orderitems.all():
            if item.size == 'S':
                item.product.stock_S += item.quantity
            elif item.size == 'M':
                item.product.stock_M += item.quantity
            elif item.size == 'L':
                item.product.stock_L += item.quantity
            elif item.size == 'XL':
                item.product.stock_XL += item.quantity
            elif item.size == 'one_size':
                item.product.stock += item.quantity
            item.product.save()
        order_items = OrderItem.objects.filter(order=order)
        order_items_data = OrderItemsSerializer(order_items, many=True).data
        subject = 'Ashion'
        message = f'Your order of code {order_id} has been cancelled Mr/Mrs.{order.first_name}, Your refund request is on its way to us, Wait for the refund mail.\n\nOrder Items:\n'
        for item in order_items_data:
            message += f'Product: {item["name"]}, Quantity: {item["quantity"]}, Size: {item["size"]}, Price: {item["price"]}\n'
        message += f'\nTotal: ${order.total_price}'
        from_email = 'admin@ashion.com'
        recipient_list = [order.email]
        send_mail(subject, message, from_email, recipient_list)
        return Response({'msg': 'Order canceled successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsDeliveryMan])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def orderDelivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.SHIPPED_STATE:
        order.status = Order.DELIVERED_STATE
        order.save()
        return Response({'msg': 'Order delivered successfully'}, status=status.HTTP_200_OK)
