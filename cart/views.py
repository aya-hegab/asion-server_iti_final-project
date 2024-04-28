from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.models import *
from .serlizer import CartSerlizer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addToCart(request):
    user = request.user.id
    item = request.data["item"]
    quantity = request.data["quantity"]
    size = request.data["size"]
    product = Product.objects.get(id=item)

    # price = product.newprice if product.sale else product.price

    if product.sizeable and size == "one_size":
        itemStock = product.stock
    if product.sizeable:
        itemStock = getattr(product, f"stock_{size}")
        # print(itemStock)
    else:
        itemStock = product.stock

    data = {'user': user, 'item': item, "quantity": quantity , "size":size}

    if Cart.objects.filter(user=user, item=item, size=size).exists():
        old_quantity = Cart.objects.filter(user=user, item=item, size=size).first().quantity
        existing_cart_item = Cart.objects.filter(user=user, item=item, size=size).first()
        if existing_cart_item:
            new_quantity = existing_cart_item.quantity + int(quantity)
            if new_quantity <= itemStock:
                existing_cart_item.quantity = new_quantity
                existing_cart_item.save()
                new_quantity = Cart.objects.filter(user=user, item=item, size=size).first().quantity
                total_item_price = existing_cart_item.get_total_item_price()
                return Response({'msg': 'Quantity updated in cart', 'total_item_price': total_item_price,'quantity': new_quantity - old_quantity}, status=status.HTTP_200_OK)
            else:
                addedQuantity = itemStock - existing_cart_item.quantity
                existing_cart_item.quantity = itemStock
                existing_cart_item.save()
                total_item_price = existing_cart_item.get_total_item_price()
                return Response({'msg': 'Quantity cannot be increased further, exceeds stock limit', 'quantity':addedQuantity}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'No item found in the cart to update'}, status=status.HTTP_404_NOT_FOUND)
    elif Cart.objects.filter(user=user, item=item).exists():
        if itemStock >= quantity:
            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save()
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price,'quantity': quantity}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "user": user,
                "item": item,
                "quantity": itemStock,
                "size": size
            }
            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save()
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price, 'quantity': itemStock }, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if itemStock >= quantity:

            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save()
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price,'quantity': quantity}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        elif itemStock == 0:
            return Response({'msg': 'out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return Response({'msg': 'Quantity exceeds stock limit'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "user": user,
                "item": item,
                "quantity": itemStock,
                "size": size
            }
            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save()
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price, 'quantity': itemStock }, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteFromCart(request, cart_id):
    obj = Cart.objects.filter(id=cart_id).first()
    if obj is not None: 
        obj.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'product not found'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def reduceCartItemQuantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if request.method == 'PUT':
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            total_item_price = cart.get_total_item_price()
            return Response({'msg': 'Quantity reduced successfully','total_item_price': total_item_price})
        else:
            return Response({'msg': 'Quantity cannot be reduced further'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def increaseCartItemQuantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if request.method == 'PUT':
        if cart.item.stock > cart.quantity:  # Check if increasing quantity exceeds stock limit
            cart.quantity += 1
            cart.save()

            # Recalculate total item price
            total_item_price = cart.get_total_item_price()

            return Response({'msg': 'Quantity increased successfully', 'total_item_price': total_item_price})
        else:
            return Response({'msg': 'Quantity cannot be increased further, exceeds stock limit'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listCartItems(request):
    user_id = request.user.id
    user_carts = Cart.objects.filter(user_id=user_id)
    serializer = CartSerlizer(user_carts, many=True)
    total_items_price = 0
    total_items_count = 0
   
    for cart_item in user_carts:
        size = cart_item.size
        if size == "one_size":
            if cart_item.item.stock == 0:
                cart_item.delete()
                user_carts.save()
        elif size == "S":
            if cart_item.item.stock_S == 0:
                cart_item.delete()
                user_carts.save()
        elif size == "M":
            if cart_item.item.stock_M == 0:
                cart_item.delete()
                user_carts.save()
        elif size == "L":
            if cart_item.item.stock_L == 0:
                cart_item.delete()
                user_carts.save()
        elif size == "XL":
            if cart_item.item.stock_XL == 0:
                cart_item.delete()
                user_carts.save()
        for cart_item in user_carts:
            total_items_price += cart_item.get_total_item_price()
            total_items_count += cart_item.quantity
        # print(size)
        # print("******************************")
    response_data = {
        'cart_items': serializer.data,
        'total_items_price': total_items_price,
        'total_items_count': total_items_count,
    }
    
    return Response(response_data)
