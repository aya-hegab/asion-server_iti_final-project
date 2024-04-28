from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
   path('allproducts/',allProducts,name='allProducts'), 
   path('allpro/',allProductwithoutpagination,name='allPro'),
   path('getProduct/<int:id>/', getproductbyid, name='getproductbyid'),
   path('addProduct/',addProduct,name='addProduct' ),
   path('updateProduct/<int:id>/', ProductUpdateAPIView.as_view(),name='updateProduct' ),
   #path('updateProduct/<int:id>/', updateProduct,name='updateProduct' ),
   path('deleteProduct/<int:id>/',deleteProduct,name='deleteProduct' ),
   path('<str:pk>/rate', addRate,name='addRate'),
]