import os
from rest_framework.views import APIView
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from product.models import *
from .serlizer import ProductsSerlizer
from django.shortcuts import get_object_or_404
from .filiters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated

parser_classes = (MultiPartParser, FormParser)


@api_view(['GET'])
def allProducts(request):
    filterproducts = ProductFilter(
        request.GET, queryset=Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 12
    queryset = paginator.paginate_queryset(filterproducts.qs, request)
    productsjson = ProductsSerlizer(queryset, many=True).data
    return paginator.get_paginated_response({'products': productsjson})


@api_view(['GET'])
def allProductwithoutpagination(request):
    products = Product.objects.all().order_by('id')
    products_json = ProductsSerlizer(products, many=True).data
    return Response({'products': products_json})


@api_view(['GET'])
def getproductbyid(request, id):
    product = get_object_or_404(Product, id=id)
    productjson = ProductsSerlizer(product, many=False).data
    return Response({'product': productjson})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addProduct(request):
   # if request.user.usertype == 'vendor':  # Check if the authenticated user is a vendor
        serializer = ProductsSerlizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'added'})
        else:
            return Response({'msg': 'wrong data', 'error': serializer.errors})
   # else:
       # return Response({'msg': 'Only vendors can add products.'}, status=status.HTTP_403_FORBIDDEN)


#@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
#def updateProductt(request, id):
#    updateobj = Product.objects.filter(id=id).first()
#    if updateobj:
#        serializedProduct = ProductsSerlizer(
#            instance=updateobj, data=request.data)
#        if serializedProduct.is_valid():
#            print(serializedProduct.validated_data)
#            serializedProduct.save()
#            return Response(data=serializedProduct.data)


class ProductUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            updateobj = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'msg': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        update_data = {
            'name': request.data.get('name', updateobj.name)[:1000],
            'description': request.data.get('description', updateobj.description)[:1000],
            'price': request.data.get('price', updateobj.price),
            'newprice': request.data.get('newprice', updateobj.newprice),
            'brand': request.data.get('brand', updateobj.brand),
            'subImageOne': request.FILES.get('subImageOne', updateobj.subImageOne),
            'subImageTwo': request.FILES.get('subImageTwo', updateobj.subImageTwo),
            'subImageThree': request.FILES.get('subImageThree', updateobj.subImageThree),
            'subImageFour': request.FILES.get('subImageFour', updateobj.subImageFour),
            'image': request.FILES.get('image', updateobj.image),
            'stock_S': int(request.data.get('stock_S', updateobj.stock_S)),
            'stock_M': int(request.data.get('stock_M', updateobj.stock_M)),
            'stock_L': int(request.data.get('stock_L', updateobj.stock_L)),
            'stock_XL': int(request.data.get('stock_XL', updateobj.stock_XL)),
            'stock': int(request.data.get('stock', updateobj.stock)),
            'sizeable': request.data.get('sizeable', updateobj.sizeable),
            'new':  request.data.get('new', updateobj.new),
            'sale': request.data.get('sale', updateobj.sale),

                                       
        }

        update_data['sizeable'] = update_data['sizeable'].lower() == 'true' if isinstance(update_data['sizeable'], str) else update_data['sizeable']
        update_data['new'] = update_data['new'].lower() == 'true' if isinstance(update_data['new'], str) else update_data['new']
        update_data['sale'] = update_data['sale'].lower() == 'true' if isinstance(update_data['sale'], str) else update_data['sale']

        # Remove previous image file if a new image is provided
        if 'image' in request.FILES and updateobj.image:
            media_file = os.path.join(os.getcwd(), updateobj.image.path)
            if os.path.isfile(media_file):
                os.remove(media_file)
                print(f"Deleted: {media_file}")

        # Remove previous sub-images if new sub-images are provided
        for sub_image_field in ['subImageOne', 'subImageTwo', 'subImageThree', 'subImageFour']:
            if sub_image_field in request.FILES and getattr(updateobj, sub_image_field):
                media_file = os.path.join(os.getcwd(), getattr(updateobj, sub_image_field).path)
                if os.path.isfile(media_file):
                    os.remove(media_file)
                    print(f"Deleted: {media_file}")


        # Update object with the new data
        for attr, value in update_data.items():
            setattr(updateobj, attr, value)

        updateobj.save()
        return Response({'msg': 'Product updated successfully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteProduct(request, id):
    pro = Product.objects.filter(id=id).first()
    if pro is not None:  # Check if pro exists
        pro.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'product not found'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addRate(request, pk):
    product = get_object_or_404(Product, id=pk)
    data = request.data

    if 'rating' not in data:
        return Response({"error": "Rating data is missing"}, status=status.HTTP_400_BAD_REQUEST)

    new_rating = data['rating']

    if new_rating <= 0 or new_rating > 5:
        return Response({"error": 'Please select between 1 to 5 only'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has already rated this product
    existing_rating = product.rates.filter(user=request.user).first()

    if existing_rating:
        # Update the existing rating
        existing_rating.rating = new_rating
        existing_rating.save()
    else:
        # Create a new rating
        Rates.objects.create(
            product=product,
            user=request.user,
            rating=new_rating,
        )

    # Recalculate the average rating for the product
    avg_rating = product.rates.aggregate(
        avg_rating=Avg('rating'))['avg_rating']
    product.ratings = avg_rating
    product.save()

    return Response({'details': 'Product rate updated'})