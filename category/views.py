from django.shortcuts import render
from .app import upload_photo, delete_photos
from rest_framework import generics
from rest_framework.views import  APIView
from .models import Category,SubCategory
from .serializers import CategorySerializer,SubCategorySerializer
import os
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class SubCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


# @api_view(['POST'])
# def Createcategory(request):


#     serializer = CategorySerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     category = serializer.save()
    
    
#     if serializer.is_valid():
    
    
#         cat = CategorySerializer(category)
#         # if user send new image
#         if 'image' in request.data and request.data['image'] is not None:
#                 # if user has already image on drive
#                 if serializer.validated_data.get('image') is not None:
#                     delete_photos(f"{category.id}.png", "1dmBbgr6MYcQpYW02stgKl3ntVkSY9T1h")
                           
#                 # upload new image
#                 media_folder = os.path.join(os.getcwd(), "media/category/images/")
#                 # save new url
#                 Url_Image = upload_photo(os.path.join(media_folder, os.path.basename(serializer['image'].value)),f"{category.id}.png", "1dmBbgr6MYcQpYW02stgKl3ntVkSY9T1h")
#                 category.imageUrl = Url_Image
#                 category.save()
                
#                 # remove image from server
#                 if os.path.exists(media_folder):
#                     for file_name in os.listdir(media_folder):
#                         file_path = os.path.join(media_folder, file_name)
#                         try:
#                             if os.path.isfile(file_path):
#                                 os.remove(file_path)
#                                 print(f"Deleted: {file_path}")
#                             else:
#                                 print(f"Skipped: {file_path} (not a file)")
#                         except Exception as e:
#                             print(f"Error deleting {file_path}: {e}")
#                 else:
#                     print("Folder does not exist.")


#         return Response({"product" : cat.data}, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    


