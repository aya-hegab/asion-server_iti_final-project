from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
   path('listReviwes/',listReviews,name='listReviwes'), 
   path('getReview/<int:id>',getReview,name='getReview'),
   path('addReview/',addReview,name='addReview'),
   path('updateReview/<int:id>',updateReview,name='updateReview'),
   path('deleteReview/<int:id>',deleteReview,name='deleteReview'),
]
