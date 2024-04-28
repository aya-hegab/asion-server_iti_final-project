from rest_framework.response import Response
from rest_framework.decorators import api_view
from review.models import *
from .serializer import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listReviews(request):
    reviews = Review.review_list()
    serializer = ReviewSerializer(reviews, many=True)
    return Response({'msg': 'accept', 'data': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getReview(request, id):
    review = Review.getReviewById(id)
    serializer = ReviewSerializer(review).data
    return Response({'msg': 'accept', 'data':  serializer})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addReview(request):
    obj = Review()
    obj = ReviewSerializer(data=request.data)
    if (obj.is_valid()):
        obj.save()
        return Response({'msg': 'added'})
    return Response({'msg': 'wrong data', 'error': obj.errors})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def updateReview(request, id):
    updateobj = Review.objects.filter(id=id).first()
    if updateobj:
        serializedReview = ReviewSerializer(
            instance=updateobj, data=request.data)
        if serializedReview.is_valid():
            serializedReview.save()  
            return Response(data=serializedReview.data)
        else:
            return Response({'errors': serializedReview.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)       


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteReview(request, id):
    review = Review.getReviewById(id)
    if review is not None:  # Check if review exists
        review.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'review not found'})