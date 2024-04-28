from django.urls import path
from .views import *

urlpatterns = [
        path('add/', addToList),
        path('delete/<int:item_id>', deleteFromList),
        path('list/', wishList),
]
