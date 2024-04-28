from django.urls import path
from .views import BannerListCreateView

from .views import DiscountListCreateView
urlpatterns = [
    path('banners/', BannerListCreateView.as_view(), name='banner-list-create'),
    path('discounts/', DiscountListCreateView.as_view(), name='discount-list-create'),
]