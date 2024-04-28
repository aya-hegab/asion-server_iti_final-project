from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from cart.models import Cart
from users.views import *
from product.models import Product   
from cart.models import Cart   
from .serializers import *
from .models import *
# checkout 
from rest_framework import response
from django.http import HttpResponse
import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
#from payment.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from django.http import Http404
from django.db import transaction
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_orders(request):
    orders = Order.objects.order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(email=user.email) .order_by('-id') # Assuming email is used to identify the user
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def vendor_orderItems(request):
    user = request.user
    try:
        items = OrderItem.objects.filter(product__vendor=user)
    except OrderItem.DoesNotExist:
        raise ValidationError({'error': 'Order items not found for this vendor'})

    serializer = OrderItemsSerializer(items, many=True)
    return Response({'order_items': serializer.data})

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shipProduct(request, product_id):
    try:    
        order_item = OrderItem.objects.get(id=product_id)
    except OrderItem.DoesNotExist:
        return Response({'error': 'Order item not found'}, status=404)
    
    order_item.isReady = True
    order_item.save()

    order = order_item.order
    if OrderItem.objects.filter(order=order).exclude(isReady=True).exists():
        # Not all items are ready, do not update the order status
        return Response({'msg': 'Product shipment status updated successfully'}, status=200)
    
    # All items are ready, update the order status to "R"
    if order.status != "C" and order.status != "F":
        order.status = 'R'
        order.save()

    return Response({'msg': 'Product shipment status updated successfully'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def shipOrder(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.READY_STATE:
        order.status = Order.SHIPPED_STATE
        order.save()
        order_items = OrderItem.objects.filter(order=order)
        order_items_data = OrderItemsSerializer(order_items, many=True).data
        subject = 'Ashion'
        message = f'Your order of code {order_id} has been shipped from Ashion on its way to you Mr/Mrs.{order.first_name}.\n\nOrder Items:\n'
        for item in order_items_data:
            message += f'Product: {item["name"]}, Quantity: {item["quantity"]}, Size: {item["size"]}, Price: {item["price"]}\n'
        message += f'\nTotal: ${order.total_price}'
        from_email = 'admin@ashion.com'
        recipient_list = [order.email]
        send_mail(subject, message, from_email, recipient_list)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def refundMoney(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.CANSCELLED_STATE or order.status == Order.FAILED_STATE:
        order.status = Order.REFUNDED_STATE
        order.save()
        order_items = OrderItem.objects.filter(order=order)
        order_items_data = OrderItemsSerializer(order_items, many=True).data
        subject = 'Ashion'
        message = f'Your order of code {order_id} will be refunded Mr/Mrs.{order.first_name} and refunds take 5-10 days.\n\nOrder Items:\n'
        for item in order_items_data:
            message += f'Product: {item["name"]}, Quantity: {item["quantity"]}, Size: {item["size"]}, Price: {item["price"]}\n'
        message += f'\nTotal: ${order.total_price}'
        from_email = 'admin@ashion.com'
        recipient_list = [order.email]
        send_mail(subject, message, from_email, recipient_list)

    serializer = OrderSerializer(order)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_ordersTmp(request):
    orders = OrderTmp.objects.all() # Fetch all OrderTmp objects
    serializer = OrderTmpSerializer(orders, many=True)  # Serialize queryset
    return Response({'orders': serializer.data})

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
def get_order(request,pk):
    order =get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_orderTmp(request):
    email = request.user.email
    
    try:
        order = OrderTmp.objects.get(email=email)
    except OrderTmp.DoesNotExist:
        raise ValidationError({'error': 'Order not found for this email'})

    serializer = OrderTmpSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def process_order(request,pk):
    order =get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
     
    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_order(request,pk):
    order =get_object_or_404(Order, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_orderTmp(request,pk):
    order =get_object_or_404(OrderTmp, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})


@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def new_orderTmp(request):
    user = request.user
    data = request.data
    order_items = data.get('order_Items', [])
    # items_to_delete = []

    if not order_items or len(order_items) == 0:
        return Response({'error': 'No order received'}, status=status.HTTP_400_BAD_REQUEST)

    zip_code = data.get('zip_code')
    if zip_code is None:
        return Response({'error': 'zip_code is required'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 0)) for item in order_items)
    
    order = OrderTmp.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=user.email,
        city=data['city'],
        zip_code=zip_code,
        street=data['street'],
        phone_number=data['phone_number'],
        country=data['country'],
        total_price=total_price,
        state=data['state'],
    )

    for i in order_items:
        try:
            with transaction.atomic():
                product = Product.objects.get(id=i['product'])
                item = OrderItemTmp.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=i['quantity'],
                    price=i.get('price', 0),  # Use .get() to handle missing 'price' key
                    size=i['size'],  # Use .get() to handle missing 'price' key
                )
                # size=i['size']
                # quantity = i['quantity']
                # if size == 'S' and product.stock_S == 0:
                #     items_to_delete.append(i)
                #     continue
                # elif size == 'M' and product.stock_M == 0:
                #     items_to_delete.append(i)
                #     continue
                # elif size == 'L' and product.stock_L == 0:
                #     items_to_delete.append(i)
                #     continue
                # elif size == 'XL' and product.stock_XL == 0:
                #     items_to_delete.append(i)
                #     continue
                # elif size == 'one_size' and product.stock == 0:
                #     items_to_delete.append(i)
                # item_price = float(i.get('price', 0)) * quantity
                # total_price += item_price

                product.save()
        except Product.DoesNotExist:
            return Response({'error': f'Product with ID {i["product"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # Delete items with zero stock from the order
    # for item_to_delete in items_to_delete:
    #     order_items.remove(item_to_delete)

    # Update total price of the order
    order.total_price = total_price
    order.save()
    serializer = OrderTmpSerializer(order, many=False)
    return Response(serializer.data)



@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data.get('order_Items', [])
    

    if not order_items or len(order_items) == 0:
        return Response({'error': 'No order received'}, status=status.HTTP_400_BAD_REQUEST)

    zip_code = data.get('zip_code')
    if zip_code is None:
        return Response({'error': 'zip_code is required'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 0)) for item in order_items)
    
    order = Order.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=user.email,
        city=data['city'],
        zip_code=zip_code,
        street=data['street'],
        phone_number=data['phone_number'],
        country=data['country'],
        total_price=total_price,
        state=data['state'],
    )

    for i in order_items:
        try:
            with transaction.atomic():
                product = Product.objects.get(id=i['product'])
                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=i['quantity'],
                    price=i.get('price', 0),  # Use .get() to handle missing 'price' key
                    size = i["size"]
                )
                
                size=i['size']  # Use .get() to handle missing 'price' key
                if size == "S" and product.stock_S >= item.quantity:
                    product.stock_S -= item.quantity
                elif size == "M" and product.stock_M >= item.quantity:
                    product.stock_M -= item.quantity
                elif size == "L" and product.stock_L >= item.quantity:
                    product.stock_L -= item.quantity
                elif size == "XL" and product.stock_XL >= item.quantity:
                    product.stock_XL -= item.quantity
                elif size == "one_size" and product.stock >= item.quantity:
                    product.stock -= item.quantity
                # else:
                #     order.total_price = total_price - (float(item.quantity) * float(item.price))
                #     order.save()
                #     item.delete() 
                    # order_items.save() # Remove the item from the order if stock is insufficient
                    # return Response({'error': f'Insufficient stock for product with ID {i["product"]}'}, status=status.HTTP_400_BAD_REQUEST)
                
                # product.stock -= item.quantity
                product.save()
        except Product.DoesNotExist:
            return Response({'error': f'Product with ID {i["product"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = Cart.objects.filter(user=user.id)
    cart_items.delete()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


'''    for i in order_items:
        product = Product.objects.get(id=i['product'])
        item = OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            quantity=i['quantity'],
            price=i['price']
        )
        product.stock -= item.quantity
        product.save()
    
    cart_items = Cart.objects.filter()
    cart_items.delete()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
'''



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cancelOrder(request, pk):
    order = get_object_or_404(Order, id=pk)

    # Check if order status is eligible for cancellation
    if order.status not in [Order.SHIPPED_STATE, Order.DELIVERED_STATE]:
        order.status = Order.CANSCELLED_STATE  # Change status to canceled
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
        message = f'Your order of code {pk} has been cancelled Mr/Mrs.{order.first_name}, Your refund request is on its way to us, Wait for the refund mail.\n\nOrder Items:\n'
        for item in order_items_data:
            message += f'Product: {item["name"]}, Quantity: {item["quantity"]}, Size: {item["size"]}, Price: {item["price"]}\n'
        message += f'\nTotal: ${order.total_price}'
        from_email = 'admin@ashion.com'
        recipient_list = [order.email]
        send_mail(subject, message, from_email, recipient_list)
        return Response({'msg': 'Order canceled successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'Order cannot be canceled, status is already shipped or delivered'}, status=status.HTTP_400_BAD_REQUEST)




#payment
stripe.api_key=settings.STRIPE_SECRET_KEY
success_url = settings.SITE_URL + 'thannk-you/'
API_URL="http/locahost:8000"
class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        # order_id=self.kwargs["pk"]
        total=self.kwargs["pk"]
        try:
            order=OrderTmp.objects.get(id=total)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'usd',
                             'unit_amount':int(order.total_price) * 100,
                             'product_data':{
                                 'name':"total",
                                 #'images':[f"{API_URL}/{orderitem_id.product_image}"]

                             }
                        },
                        'quantity': 1,
                    },
                ],
                # metadata={
                #     "order_id":order.id
                # },
                mode='payment',
                success_url=success_url,  # Updated success_url
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)
        

from django.db.models import Sum, Count
from django.http import JsonResponse

def order_statistics(request):
    # Calculate total orders
    total_orders = Order.objects.count()

    # Calculate total revenue
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Calculate average order value
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Prepare data for visualization
    statistics_data = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'average_order_value': average_order_value,
    }

    return JsonResponse(statistics_data)

def best_selling_products(request):
    # Aggregate the quantity sold for each product
    best_selling_products = OrderItem.objects.values('product').annotate(
        total_quantity_sold=Sum('quantity')
    ).order_by('-total_quantity_sold')[:10]  # Get the top 10 best-selling products

    # Prepare data for visualization
    products_data = []
    for item in best_selling_products:
        product = Product.objects.get(id=item['product'])
        products_data.append({
            'product_name': product.name,
            'total_quantity_sold': item['total_quantity_sold'],
        })

    return JsonResponse({'best_selling_products': products_data})	