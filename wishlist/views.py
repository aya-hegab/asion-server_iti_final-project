from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wishlist.models import *
from .serlizer import WishlistSerlizer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addToList(request):
  user = request.user.id
  item = request.data["item"]
  if Wishlist.objects.filter(user=user, item=item).exists():
        Wishlist.objects.filter(user=user, item=item).delete()
        return Response({'msg': 'Item removed from wishlist'})
  else:
      wishlist_data = {'user': user, 'item': item}
      serializer = WishlistSerlizer(data=wishlist_data)
      if serializer.is_valid():
          serializer.save()
          return Response({'msg': 'Item added to wishlist'}, status=status.HTTP_201_CREATED)
      else:
          return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteFromList(request,item_id):
  obj = Wishlist.objects.filter(id=item_id).first()
  if obj is not None: 
      obj.delete()
      return Response({'msg': 'deleted'})
  return Response({'msg': 'product not found'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def wishList(request):
    user_id = request.user.id
    user_list = Wishlist.objects.filter(user_id=user_id)
    serializer = WishlistSerlizer(user_list, many=True)
    
    total_items_count = user_list.count()
    
    response_data = {
        'wishlist_items': serializer.data,
        'total_items_count': total_items_count,
    }
    
    return Response(response_data, status=status.HTTP_200_OK)